# Document Automation Agent (เวอร์ชันของฉัน)

โปรแกรม Python ที่อ่านงานจากไฟล์ JSON แล้วทำเอกสารให้อัตโนมัติ:
สร้างรายงาน Word จาก template, ใส่ลายน้ำ PDF, รวม PDF และดึงข้อความจาก Word/PDF
พร้อมบันทึก audit log ทุกครั้งที่รัน

## วิธีใช้

```bash
pip install -r requirements.txt
python scripts/make_samples.py   # สร้าง template และ PDF ตัวอย่าง (ทำครั้งเดียว)
python main.py                   # รันทุก task
python main.py --only merge_pdfs apply_pdf_watermark   # รันเฉพาะบางประเภท
python -m unittest discover tests -v                   # ทดสอบ
```

## แก้ให้เป็นของตัวเอง (ทำที่ `configs/document_automation_config.json`)

- `global_data.AUTHOR_NAME` / `COMPANY_NAME`: ใส่ชื่อและหน่วยงานของคุณ
- `global_data.REPORT_DATE`: ใส่ `"auto"` เพื่อใช้วันที่วันนี้ หรือกำหนดเอง
- `data` และ `table_data` ในงานรายงาน: เปลี่ยนหัวข้อ/เนื้อหา/ตาราง หรือใช้ `"table_csv": "documents/data.csv"` แทน
- ปิดงานชั่วคราวด้วย `"enabled": false`
- ลายน้ำ: `mode` เป็น `center` หรือ `tiled`
- แก้หน้าตา template: เปิด `templates/report_template.docx` ใน Word แล้วแก้ได้เลย
  โดยเก็บ `{{ชื่อ_PLACEHOLDER}}` ไว้ (ตัวพิมพ์ใหญ่ ขีดล่าง และ `{{TABLE_PLACEHOLDER}}` คือตำแหน่งตาราง)

## โครงสร้าง

```
main.py                  จุดเริ่มต้น (CLI)
configs/                 ไฟล์ config
src/config_parser.py     ตรวจ config + แปลง path
src/document_agent.py    ตัวคุมงาน (registry ของ task)
src/word_tasks.py        งาน Word
src/pdf_tasks.py         งาน PDF
src/utils.py             logging + audit log
scripts/make_samples.py  สร้างไฟล์ตั้งต้น
tests/                   unit tests
```

## ต่างจากตัวอย่างต้นฉบับอย่างไร

บั๊กที่แก้:
- ค่าที่เติมใน Word เคยมี `{{ }}` ค้างอยู่ (เช่น `{{Monthly Performance Summary}}`) ตอนนี้แทนที่ได้ถูกต้อง
- ตารางเคยไปต่อท้ายเอกสาร ตอนนี้แทรกตรงตำแหน่ง `{{TABLE_PLACEHOLDER}}`
- ลายน้ำเคยใช้ขนาด A4 ตายตัว ตอนนี้ปรับตามขนาดของแต่ละหน้า และไม่สร้างไฟล์ชั่วคราว
- `check_required_files` เคยอ้าง task ตามลำดับ index ทำให้พังถ้าสลับลำดับใน config
- `requirements.txt` เคยว่างเปล่า / ใช้ PyPDF2 ที่เลิกพัฒนา เปลี่ยนเป็น `pypdf`
- audit log เคยเก็บ path เต็มของเครื่อง ตอนนี้เก็บแบบ relative

ที่ปรับปรุง:
- เพิ่ม CLI (`--config`, `--only`), `enabled`, `table_csv`, ลายน้ำแบบ `tiled`
- แยก task แบบ registry ไม่ใช้ if/elif ยาว และ task หนึ่งพังไม่ทำให้ตัวอื่นหยุด
- ตรวจ config ครบทุกประเภท task และคืน exit code 1 เมื่อมี task ล้มเหลว
- ดึงข้อความจาก Word ตามลำดับจริง (ย่อหน้ากับตารางสลับกันถูกที่)

ข้อจำกัด: ลายน้ำใช้ฟอนต์ Helvetica จึงรองรับเฉพาะตัวอักษรละติน
ถ้าต้องการลายน้ำภาษาไทย ต้อง register ฟอนต์ TTF ไทยกับ reportlab เพิ่ม
