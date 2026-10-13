"""อ่าน + ตรวจสอบ config และแปลง path ทั้งหมดให้เป็น absolute"""
import json
from pathlib import Path

from .utils import setup_logging

logger = setup_logging(__name__)

# ฟิลด์ที่แต่ละประเภทงานต้องมี
REQUIRED_FIELDS = {
    "generate_word_report": ["template_path", "output_path"],
    "apply_pdf_watermark": ["input_pdf", "output_pdf", "watermark_text"],
    "merge_pdfs": ["input_pdfs", "output_pdf"],
    "extract_pdf_text": ["input_pdf", "output_text_file"],
    "extract_word_text": ["input_docx", "output_text_file"],
}

PATH_KEYS = {
    "template_path", "output_path", "input_pdf", "output_pdf",
    "input_docx", "output_text_file", "table_csv",
}
PATH_LIST_KEYS = {"input_pdfs"}


class ConfigParser:
    def __init__(self, config_path, base_dir):
        self.config_path = Path(config_path)
        self.base_dir = Path(base_dir)

    def load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"ไม่พบไฟล์ config: {self.config_path}")
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"ไฟล์ config เป็น JSON ที่ไม่ถูกต้อง: {e}") from e

        self._validate(config)
        self._resolve_paths(config)
        logger.info("โหลด config สำเร็จ (%d tasks)", len(config["tasks"]))
        return config

    def _validate(self, config):
        for field in ("global_data", "tasks"):
            if field not in config:
                raise ValueError(f"config ขาดฟิลด์ '{field}'")
        if not isinstance(config["tasks"], list):
            raise ValueError("'tasks' ต้องเป็น list")

        for i, task in enumerate(config["tasks"], start=1):
            task_type = task.get("type")
            if task_type not in REQUIRED_FIELDS:
                raise ValueError(
                    f"Task #{i}: type '{task_type}' ไม่รู้จัก "
                    f"(ใช้ได้: {', '.join(REQUIRED_FIELDS)})"
                )
            missing = [k for k in REQUIRED_FIELDS[task_type] if k not in task]
            if missing:
                raise ValueError(f"Task #{i} ({task_type}) ขาดฟิลด์: {', '.join(missing)}")

    def _resolve_paths(self, config):
        for task in config["tasks"]:
            for key in PATH_KEYS & task.keys():
                task[key] = str(self.base_dir / task[key])
            for key in PATH_LIST_KEYS & task.keys():
                task[key] = [str(self.base_dir / p) for p in task[key]]
        config["audit_dir"] = str(self.base_dir / config.get("audit_dir", "documents/reports"))
