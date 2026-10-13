"""Document Agent: อ่าน task จาก config แล้วเรียก handler ที่ตรงกับ type"""
import datetime
import time
from pathlib import Path

from .pdf_tasks import PDFTasks
from .utils import AuditLog, ensure_directory_exists, relative_to_base, setup_logging
from .word_tasks import WordTasks

logger = setup_logging(__name__)


class DocumentAgent:
    def __init__(self, config):
        self.config = config
        self.audit = AuditLog()
        self.pdf = PDFTasks()
        self.word = WordTasks()
        self.global_data = self._prepare_global_data(config.get("global_data", {}))
        # registry: type -> method  (เพิ่มงานใหม่แค่เพิ่มบรรทัดเดียว)
        self.handlers = {
            "generate_word_report": self._generate_word_report,
            "apply_pdf_watermark": self._apply_pdf_watermark,
            "merge_pdfs": self._merge_pdfs,
            "extract_pdf_text": self._extract_pdf_text,
            "extract_word_text": self._extract_word_text,
        }

    @staticmethod
    def _prepare_global_data(data):
        data = dict(data)
        if str(data.get("REPORT_DATE", "")).lower() == "auto":
            data["REPORT_DATE"] = datetime.date.today().isoformat()
        return data

    # ---------- handlers (คืนค่า True/False) ----------
    def _generate_word_report(self, t):
        placeholders = {**self.global_data, **t.get("data", {})}
        return self.word.generate_report_from_template(
            t["template_path"], t["output_path"], placeholders,
            t.get("table_data"), t.get("table_csv"),
        )

    def _apply_pdf_watermark(self, t):
        return self.pdf.apply_watermark(
            t["input_pdf"], t["output_pdf"], t["watermark_text"],
            t.get("font_size", 50), t.get("color", [0.5, 0.5, 0.5, 0.2]),
            t.get("angle", 45), t.get("mode", "center"),
        )

    def _merge_pdfs(self, t):
        return self.pdf.merge_pdfs(t["input_pdfs"], t["output_pdf"])

    @staticmethod
    def _write_text(text, path):
        if text is None:
            return False
        ensure_directory_exists(Path(path).parent)
        Path(path).write_text(text, encoding="utf-8")
        logger.info("บันทึกข้อความ -> %s", path)
        return True

    def _extract_pdf_text(self, t):
        return self._write_text(self.pdf.extract_text_from_pdf(t["input_pdf"]), t["output_text_file"])

    def _extract_word_text(self, t):
        return self._write_text(self.word.extract_text_from_word(t["input_docx"]), t["output_text_file"])

    # ---------- runner ----------
    def _process_task(self, task):
        name = task.get("name", task["type"])
        if task.get("enabled", True) is False:
            self.audit.add("SKIPPED", f"ข้าม '{name}' (enabled=false)", task["type"])
            return "skipped"
        self.audit.add("INFO", f"เริ่ม '{name}'", task["type"])
        try:
            ok = self.handlers[task["type"]](task)
        except Exception as e:  # task หนึ่งพังไม่ควรทำให้ทั้งระบบหยุด
            logger.exception("task '%s' error", name)
            self.audit.add("ERROR", f"'{name}' error: {e}", task["type"])
            return "failed"
        self.audit.add("SUCCESS" if ok else "ERROR",
                       f"'{name}' {'สำเร็จ' if ok else 'ล้มเหลว'}", task["type"])
        return "success" if ok else "failed"

    def run(self, only_types=None):
        started = time.perf_counter()
        self.audit.add("INFO", "Document Agent เริ่มทำงาน")
        result = {"success": 0, "failed": 0, "skipped": 0}
        for task in self.config["tasks"]:
            if only_types and task["type"] not in only_types:
                continue
            result[self._process_task(task)] += 1

        elapsed = time.perf_counter() - started
        self.audit.add("INFO", f"เสร็จสิ้นใน {elapsed:.2f}s", "summary", result)
        report = self.audit.save(self.config["audit_dir"])
        logger.info("สรุป: สำเร็จ %(success)d | ล้มเหลว %(failed)d | ข้าม %(skipped)d", result)
        logger.info("audit report: %s", relative_to_base(report))
        return result
