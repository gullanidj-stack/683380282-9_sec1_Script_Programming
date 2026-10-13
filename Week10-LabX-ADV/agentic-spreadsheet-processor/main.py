# main.py
import os

from src.utils import setup_logging
from src.config_parser import ConfigParser
from src.spreadsheet_agent import SpreadsheetAgent

logger = setup_logging(__name__)


def main():
    """Entry point: loads the config and runs the Spreadsheet Agent."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)  # config paths like 'data/...' are relative to the project root
    config_file_path = os.path.join(base_dir, 'configs', 'example_spreadsheet_config.json')

    try:
        os.makedirs('data', exist_ok=True)
        logger.info(f"Loading configuration from: {config_file_path}")
        config = ConfigParser(config_file_path).load_config()

        input_file_path = config.get("input_file")
        if not os.path.exists(input_file_path):
            logger.critical(f"Input Excel file not found: '{input_file_path}'. Please create it with sample data.")
            return

        logger.info("Running Spreadsheet Agent...")
        SpreadsheetAgent(config).run()
    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
