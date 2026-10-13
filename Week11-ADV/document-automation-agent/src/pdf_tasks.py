"""งานเกี่ยวกับไฟล์ PDF: watermark, merge, ดึงข้อความ"""
import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

from .utils import ensure_directory_exists, setup_logging

logger = setup_logging(__name__)

FONT = "Helvetica-Bold"


class PDFTasks:
    @staticmethod
    def _watermark_overlay(width, height, text, font_size, color, angle, mode):
        """สร้างหน้า overlay ขนาดเท่าหน้าจริง (ตัวอย่างเดิมล็อกไว้ที่ A4 เท่านั้น)"""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))
        r, g, b, a = color
        c.setFillColor(Color(r, g, b, alpha=a))
        c.setFont(FONT, font_size)
        text_width = c.stringWidth(text, FONT, font_size)

        if mode == "tiled":
            step_x, step_y = text_width + font_size * 2, font_size * 4
            y = -height
            while y < height * 2:
                x = -width
                while x < width * 2:
                    c.saveState()
                    c.translate(x, y)
                    c.rotate(angle)
                    c.drawString(0, 0, text)
                    c.restoreState()
                    x += step_x
                y += step_y
        else:  # center
            c.translate(width / 2, height / 2)
            c.rotate(angle)
            c.drawString(-text_width / 2, -font_size / 4, text)

        c.showPage()
        c.save()
        buffer.seek(0)
        return PdfReader(buffer).pages[0]

    def apply_watermark(self, input_pdf, output_pdf, text, font_size=50,
                        color=(0.5, 0.5, 0.5, 0.2), angle=45, mode="center"):
        if not Path(input_pdf).exists():
            logger.error("ไม่พบ PDF ต้นฉบับ: %s", input_pdf)
            return False
        reader, writer = PdfReader(input_pdf), PdfWriter()
        for page in reader.pages:
            w, h = float(page.mediabox.width), float(page.mediabox.height)
            page.merge_page(self._watermark_overlay(w, h, text, font_size, tuple(color), angle, mode))
            writer.add_page(page)
        ensure_directory_exists(Path(output_pdf).parent)
        with open(output_pdf, "wb") as f:
            writer.write(f)
        logger.info("ใส่ watermark '%s' ให้ %d หน้า -> %s", text, len(reader.pages), output_pdf)
        return True

    def merge_pdfs(self, pdf_paths, output_pdf):
        writer = PdfWriter()
        for path in pdf_paths:
            if not Path(path).exists():
                logger.warning("ข้ามไฟล์ที่ไม่มีอยู่: %s", path)
                continue
            for page in PdfReader(path).pages:
                writer.add_page(page)
        if len(writer.pages) == 0:
            logger.error("ไม่มีหน้าให้รวมเลย")
            return False
        ensure_directory_exists(Path(output_pdf).parent)
        with open(output_pdf, "wb") as f:
            writer.write(f)
        logger.info("รวม PDF %d หน้า -> %s", len(writer.pages), output_pdf)
        return True

    def extract_text_from_pdf(self, pdf_path):
        if not Path(pdf_path).exists():
            logger.error("ไม่พบ PDF: %s", pdf_path)
            return None
        reader = PdfReader(pdf_path)
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
        if not any(pages):
            logger.warning("PDF นี้ไม่มี text layer (อาจเป็นไฟล์สแกน ต้องใช้ OCR)")
        return "\n".join(f"--- Page {n} ---\n{text}\n" for n, text in enumerate(pages, start=1))
