# src/conversion_tasks.py
import json
from .utils import setup_logging

logger = setup_logging(__name__)


class ConversionTasks:
    """Conversions between CSV (list of dicts) and JSON formats."""

    def __init__(self):
        logger.info("ConversionTasks initialized.")

    def csv_to_json(self, csv_data):
        """Convert CSV rows to JSON-compatible dicts; numeric strings become numbers."""
        if not csv_data:
            logger.warning("No CSV data to convert to JSON.")
            return []

        json_data = []
        for row in csv_data:
            json_row = {}
            for key, value in row.items():
                try:
                    v = value.strip()
                    if v.isdigit():
                        json_row[key] = int(v)
                    elif v.replace('.', '', 1).isdigit():
                        json_row[key] = float(v)
                    elif v.lower() in ['true', 'false']:
                        json_row[key] = v.lower() == 'true'
                    elif v.lower() == 'null' or v == '':
                        json_row[key] = None
                    else:
                        json_row[key] = v
                except Exception as e:
                    logger.debug(f"Could not convert '{value}' for key '{key}': {e}")
                    json_row[key] = value
            json_data.append(json_row)
        logger.info(f"Converted {len(csv_data)} CSV rows to JSON format.")
        return json_data

    def json_to_csv(self, json_data, fieldnames=None):
        """Convert JSON objects to CSV-ready rows; flattens one level of nesting (details.brand)."""
        if not json_data:
            logger.warning("No JSON data to convert to CSV.")
            return [], []

        if fieldnames is None:
            keys = set()
            for item in json_data:
                for k, v in item.items():
                    if isinstance(v, dict):
                        keys.update(f"{k}.{sub}" for sub in v)
                    else:
                        keys.add(k)
            fieldnames = sorted(keys)
            logger.info(f"Inferred fieldnames for JSON to CSV: {fieldnames}")

        rows = []
        for item in json_data:
            row = {}
            for field in fieldnames:
                if '.' in field:
                    parent, child = field.split('.', 1)
                    cur = item.get(parent)
                    row[field] = cur.get(child, '') if isinstance(cur, dict) else ''
                else:
                    value = item.get(field, '')
                    row[field] = json.dumps(value) if isinstance(value, (dict, list)) else value
            rows.append(row)
        logger.info(f"Converted {len(json_data)} JSON objects to CSV format.")
        return rows, fieldnames
