import logging
import os


def setup_logging(name, level=logging.INFO):
    """Return a logger with a single console handler."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:  # avoid duplicate handlers (and duplicate log lines)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
    logger.propagate = False
    return logger


_logger = setup_logging(__name__)


def ensure_directory_exists(path):
    """Create a directory if it does not exist."""
    try:
        os.makedirs(path, exist_ok=True)
        _logger.info(f"Directory ensured: {path}")
    except OSError as e:
        _logger.error(f"Error creating directory {path}: {e}")
        raise