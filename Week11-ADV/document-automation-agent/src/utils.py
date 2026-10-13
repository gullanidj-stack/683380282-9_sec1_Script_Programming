"""ฟังก์ชันช่วยเหลือทั่วไป: logging, จัดการโฟลเดอร์, และ audit log"""
import datetime
import json
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def setup_logging(name, level=logging.INFO):
    """สร้าง logger ที่ไม่พิมพ์ซ้ำสองรอบ (ต่างจากตัวอย่างที่ใช้ basicConfig + handler พร้อมกัน)"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", "%H:%M:%S")
        )
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel(level)
    return logger


def ensure_directory_exists(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def relative_to_base(path):
    """แปลง path เป็นแบบ relative เพื่อไม่ให้ audit log เผย path ในเครื่องของเรา"""
    try:
        return str(Path(path).resolve().relative_to(BASE_DIR))
    except ValueError:
        return str(path)


class AuditLog:
    """เก็บบันทึกการทำงานของ agent แล้วเซฟเป็น JSON"""

    def __init__(self):
        self.entries = []

    def add(self, status, message, task_type="agent", details=None):
        self.entries.append(
            {
                "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
                "status": status,
                "task_type": task_type,
                "message": message,
                "details": details or {},
            }
        )

    def save(self, directory):
        ensure_directory_exists(directory)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path(directory) / f"audit_report_{stamp}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2, ensure_ascii=False)
        return path
