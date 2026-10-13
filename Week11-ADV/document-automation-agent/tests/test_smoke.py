"""รัน:  python -m unittest discover tests -v"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import docx  # noqa: E402
from pypdf import PdfReader  # noqa: E402

from src.pdf_tasks import PDFTasks  # noqa: E402
from src.word_tasks import WordTasks  # noqa: E402

TEMPLATE = ROOT / "templates" / "report_template.docx"
SOURCE = ROOT / "documents" / "source_document.pdf"


class WordTests(unittest.TestCase):
    def test_placeholders_replaced_without_braces_and_table_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "r.docx"
            ok = WordTasks().generate_report_from_template(
                str(TEMPLATE), str(out),
                {"REPORT_TITLE": "T", "REPORT_DATE": "D", "AUTHOR_NAME": "A",
                 "COMPANY_NAME": "C", "INTRODUCTION_TEXT": "I", "MONTH_PERIOD": "M"},
                [["h1", "h2"], ["a", "b"]],
            )
            self.assertTrue(ok)
            text = WordTasks().extract_text_from_word(str(out))
            self.assertNotIn("{{", text)
            lines = text.splitlines()
            # ตารางต้องอยู่ก่อนหัวข้อ "สรุป" (ไม่ใช่ท้ายเอกสาร)
            self.assertLess(lines.index("h1\th2"), lines.index("สรุป"))


class PdfTests(unittest.TestCase):
    def test_watermark_and_merge(self):
        with tempfile.TemporaryDirectory() as tmp:
            wm = Path(tmp) / "wm.pdf"
            self.assertTrue(PDFTasks().apply_watermark(str(SOURCE), str(wm), "X", 40))
            self.assertEqual(len(PdfReader(str(wm)).pages), len(PdfReader(str(SOURCE)).pages))
            merged = Path(tmp) / "m.pdf"
            self.assertTrue(PDFTasks().merge_pdfs([str(SOURCE), str(wm)], str(merged)))
            self.assertEqual(len(PdfReader(str(merged)).pages),
                             2 * len(PdfReader(str(SOURCE)).pages))

    def test_missing_input_returns_false(self):
        self.assertFalse(PDFTasks().apply_watermark("nope.pdf", "out.pdf", "X"))


if __name__ == "__main__":
    unittest.main()
