# ============================================================
# utils.py — Logging and shared helpers
# ============================================================

import logging
import os
from datetime import datetime
from config import LOG_DIR, OUTPUT_DIR


def setup_logger(name: str) -> logging.Logger:
    """Create a logger that writes to both console and a dated log file."""
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    # File handler — one log file per day
    log_file = os.path.join(LOG_DIR, f"pipeline_{datetime.now():%Y%m%d}.log")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def ensure_output_dir():
    """Create the outputs/ folder if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_csv(df, filename: str, logger=None):
    """Save a DataFrame to outputs/ and log the action."""
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(path, index=False)
    if logger:
        logger.info(f"Saved {len(df):,} rows → {path}")
    return path
