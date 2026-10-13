# src/config_parser.py
import json
import os
from .utils import setup_logging

logger = setup_logging(__name__)


class ConfigParser:
    """Parses and validates the data automation configuration from a JSON file."""

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        if not os.path.exists(self.config_path):
            logger.critical(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            logger.critical(f"Invalid JSON format in config file: {e}")
            raise ValueError(f"Invalid JSON format in config file: {e}")
        self._validate_config()
        logger.info(f"Configuration loaded successfully from {self.config_path}")
        return self.config

    def _validate_config(self):
        if "tasks" not in self.config:
            raise ValueError("Missing required field in config: 'tasks'")
        if not isinstance(self.config["tasks"], list):
            raise ValueError("Config field 'tasks' must be a list.")

        for i, task in enumerate(self.config["tasks"]):
            if "type" not in task:
                raise ValueError(f"Task {i} is missing 'type' field.")
            t = task["type"]

            # NOTE: 'output_data_key' is NOT required for every task
            # (save_csv / save_json produce files, not data).
            if t in ["load_csv", "load_json"]:
                for k in ("file_path", "output_data_key"):
                    if k not in task:
                        raise ValueError(f"Task {i} (type: {t}) requires '{k}'.")
            if t in ["save_csv", "save_json"]:
                for k in ("file_path", "input_data_key"):
                    if k not in task:
                        raise ValueError(f"Task {i} (type: {t}) requires '{k}'.")
            if t in ["transform_csv_aggregate", "filter_csv", "update_json_data",
                     "query_json_data", "csv_to_json_conversion", "json_to_csv_conversion"]:
                if "input_data_key" not in task:
                    raise ValueError(f"Task {i} (type: {t}) requires 'input_data_key'.")
        logger.info("Configuration validated.")
