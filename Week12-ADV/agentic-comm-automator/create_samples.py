from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook

# --- สร้าง sales_report.pdf ---
c = canvas.Canvas("data/sales_report.pdf", pagesize=A4)
c.setFont("Helvetica-Bold", 18)
c.drawString(72, 780, "Sales Report (Sample)")
c.setFont("Helvetica", 12)
c.drawString(72, 750, "Month: January 2026")
c.drawString(72, 730, "Total Sales: 125,000 THB")
c.drawString(72, 710, "Top Product: Widget A")
c.save()

# --- สร้าง summary_data.xlsx ---
wb = Workbook()
ws = wb.active
ws.title = "Summary"
ws.append(["Product", "Units Sold", "Revenue (THB)"])
ws.append(["Widget A", 120, 60000])
ws.append(["Widget B", 80, 40000])
ws.append(["Widget C", 50, 25000])
wb.save("data/summary_data.xlsx")

print("สร้างไฟล์ตัวอย่างเรียบร้อย")