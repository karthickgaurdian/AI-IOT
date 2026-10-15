"""
Logger Module
Handles logging configuration and setup.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logger(
    level: str = "INFO",
    log_file: str = "logs/companion_cube.log",
    max_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Setup and configure logger.
    
    Args:
        level (str): Logging level
        log_file (str): Path to log file
        max_size (int): Maximum log file size in bytes
        backup_count (int): Number of backup files to keep
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("companion_cube")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Create file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_size,
        backupCount=backup_count
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get logger instance.
    
    Args:
        name (Optional[str]): Logger name
        
    Returns:
        logging.Logger: Logger instance
    """
    if name:
        return logging.getLogger(f"companion_cube.{name}")
    return logging.getLogger("companion_cube")

class LoggerAdapter(logging.LoggerAdapter):
    """Custom logger adapter for adding context to log messages."""
    
    def __init__(self, logger: logging.Logger, extra: dict):
        """
        Initialize logger adapter.
        
        Args:
            logger (logging.Logger): Logger instance
            extra (dict): Extra context to add to log messages
        """
        super().__init__(logger, extra)
    
    def process(self, msg: str, kwargs: dict) -> tuple:
        """
        Process log message and add context.
        
        Args:
            msg (str): Log message
            kwargs (dict): Logging keyword arguments
            
        Returns:
            tuple: Processed message and kwargs
        """
        # Add context to message
        context = " ".join(f"{k}={v}" for k, v in self.extra.items())
        if context:
            msg = f"{msg} [{context}]"
        return msg, kwargs

def create_logger_adapter(
    logger: logging.Logger,
    **context
) -> LoggerAdapter:
    """
    Create logger adapter with context.
    
    Args:
        logger (logging.Logger): Logger instance
        **context: Context to add to log messages
        
    Returns:
        LoggerAdapter: Logger adapter instance
    """
    return LoggerAdapter(logger, context) 