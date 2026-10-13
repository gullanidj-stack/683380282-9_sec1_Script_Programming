# main.py
import os

from src.config_parser import ConfigParser
from src.data_agent import DataAgent
from src.utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)


def check_required_input_files(config):
    """Checks that every input file used by load tasks exists before the agent starts."""
    ok = True
    for task in config['tasks']:
        if task['type'] in ['load_csv', 'load_json'] and not os.path.exists(task['file_path']):
            logger.critical(f"Required input file '{task['file_path']}' not found "
                            f"for task '{task.get('name', task['type'])}'.")
            ok = False
    return ok


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(base_dir, 'configs', 'data_pipeline_config.json')

    try:
        for folder in ('data', 'configs', 'reports'):
            ensure_directory_exists(os.path.join(base_dir, folder))

        logger.info(f"Loading configuration from: {config_file_path}")
        config = ConfigParser(config_file_path).load_config()

        # Make config file paths absolute (relative to project root)
        for task in config['tasks']:
            if 'file_path' in task:
                task['file_path'] = os.path.join(base_dir, task['file_path'])

        if not check_required_input_files(config):
            logger.critical("One or more required input files are missing. Create them in the data/ folder.")
            return

        agent = DataAgent(config)
        agent.run()
        logger.info("Data automation process completed.")

    except FileNotFoundError as e:
        logger.critical(f"File system error: {e}")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
