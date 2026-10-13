"""จุดเริ่มต้นของโปรแกรม:  python main.py [--config ...] [--only TYPE ...]"""
import argparse
import sys
from pathlib import Path

from src.config_parser import REQUIRED_FIELDS, ConfigParser
from src.document_agent import DocumentAgent
from src.utils import BASE_DIR, ensure_directory_exists, setup_logging

logger = setup_logging("main")
DEFAULT_CONFIG = BASE_DIR / "configs" / "document_automation_config.json"


def preflight(config):
    """เช็กไฟล์ input ล่วงหน้า (แจ้งเตือนอย่างเดียว ไม่หยุดทั้งระบบ)"""
    produced = {t.get("output_path") or t.get("output_pdf") for t in config["tasks"]}
    for task in config["tasks"]:
        inputs = [task.get(k) for k in ("template_path", "input_pdf", "input_docx", "table_csv")]
        inputs += task.get("input_pdfs", [])
        for path in filter(None, inputs):
            if path not in produced and not Path(path).exists():
                logger.warning("ไม่พบไฟล์ input ของ '%s': %s", task.get("name", task["type"]), path)


def parse_args(argv):
    p = argparse.ArgumentParser(description="Document Automation Agent")
    p.add_argument("--config", default=str(DEFAULT_CONFIG), help="path ของไฟล์ config (JSON)")
    p.add_argument("--only", nargs="+", choices=sorted(REQUIRED_FIELDS),
                   help="รันเฉพาะ task ประเภทที่ระบุ")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    ensure_directory_exists(BASE_DIR / "documents")
    config = ConfigParser(args.config, BASE_DIR).load_config()
    preflight(config)
    result = DocumentAgent(config).run(only_types=set(args.only) if args.only else None)
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
