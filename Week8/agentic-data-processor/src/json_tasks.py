# src/json_tasks.py
import json
import os
from .utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


class JSONTasks:
    """Advanced reading, writing, and manipulation of JSON data."""

    def __init__(self):
        logger.info("JSONTasks initialized.")

    def load_json(self, file_path):
        if not os.path.exists(file_path):
            logger.error(f"JSON file not found: {file_path}")
            return None
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info(f"Successfully loaded JSON from '{file_path}'.")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in '{file_path}': {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading JSON file '{file_path}': {e}")
            return None

    def save_json(self, data, file_path, indent=2):
        ensure_directory_exists(os.path.dirname(file_path))
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            logger.info(f"Successfully saved JSON to '{file_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON file '{file_path}': {e}")
            return False

    @staticmethod
    def _child(node, key):
        """Return the child of `node` for `key`, or None.
        dict -> by key | list -> by index ('0') or by item 'id' ('PROD001')."""
        if isinstance(node, dict):
            return node.get(key)
        if isinstance(node, list):
            if key.isdigit():
                i = int(key)
                return node[i] if 0 <= i < len(node) else None
            for item in node:
                if isinstance(item, dict) and item.get("id") == key:
                    return item
        return None

    def update_json_data(self, data, updates):
        """
        Applies updates to a JSON-like object.
        updates: [{"path": "0.stock", "value": 75, "operation": "set"}, ...]
        operations: set | add_to_list | remove_from_list
        path "" + add_to_list  -> append to the root list.
        """
        if not data:
            logger.warning("No JSON data provided for update.")
            return data

        modified = json.loads(json.dumps(data))  # deep copy

        for update in updates:
            path = update.get("path", "")
            value = update.get("value")
            operation = update.get("operation", "set")

            # Root-level list append (path is empty)
            if path == "":
                if operation == "add_to_list" and isinstance(modified, list):
                    modified.append(value)
                    logger.info("Added new item to root list.")
                else:
                    logger.warning(f"Update skipped: empty 'path' only supports add_to_list on a root list: {update}")
                continue

            keys = path.split('.')
            node = modified
            try:
                for key in keys[:-1]:
                    node = self._child(node, key)
                    if node is None:
                        break
                if node is None:
                    logger.warning(f"Path '{path}' not found. Skipping update: {update}")
                    continue

                target = keys[-1]
                if operation == "set":
                    if isinstance(node, dict):
                        node[target] = value
                        logger.info(f"Set '{path}' to '{value}'.")
                    elif isinstance(node, list) and target.isdigit() and 0 <= int(target) < len(node):
                        node[int(target)] = value
                        logger.info(f"Set '{path}' (list index) to '{value}'.")
                    else:
                        logger.warning(f"Cannot 'set' path '{path}'. Skipping: {update}")
                elif operation in ("add_to_list", "remove_from_list"):
                    lst = node.get(target) if isinstance(node, dict) else None
                    if not isinstance(lst, list):
                        logger.warning(f"Cannot {operation} for '{path}': target is not a list. Skipping: {update}")
                    elif operation == "add_to_list":
                        lst.append(value)
                        logger.info(f"Added '{value}' to list at '{path}'.")
                    elif value in lst:
                        lst.remove(value)
                        logger.info(f"Removed '{value}' from list at '{path}'.")
                    else:
                        logger.warning(f"Value '{value}' not in list at '{path}'.")
                else:
                    logger.warning(f"Unsupported operation '{operation}' for '{path}'.")
            except Exception as e:
                logger.error(f"Error applying JSON update for path '{path}': {e}. Update: {update}")

        return modified

    def query_json_data(self, data, path):
        """Query a nested element using dot-notation. Returns value or None."""
        if not data:
            logger.warning("No JSON data to query.")
            return None
        node = data
        for key in path.split('.'):
            node = self._child(node, key)
            if node is None:
                logger.warning(f"Query path '{path}' not found at key '{key}'.")
                return None
        logger.info(f"Successfully queried '{path}'. Result: {node}")
        return node
