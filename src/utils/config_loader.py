"""
Configuration Loader Module
Handles loading and validation of configuration files.
"""

import json
import os
import logging
from typing import Dict, Any
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.json"):
        """
        Initialize configuration loader.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.config = None

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        try:
            if not os.path.exists(self.config_path):
                self.logger.error(f"Configuration file not found: {self.config_path}")
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            
            self._validate_config()
            self.logger.info("Configuration loaded successfully")
            return self.config
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise

    def _validate_config(self):
        """Validate configuration structure and values."""
        required_sections = [
            'hardware',
            'ai',
            'security',
            'voice',
            'logging',
            'storage'
        ]

        # Check required sections
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required section in config: {section}")

        # Validate hardware configuration
        if 'esp32' not in self.config['hardware']:
            raise ValueError("Missing ESP32 configuration in hardware section")

        # Validate AI configuration
        if 'speech_recognition' not in self.config['ai']:
            raise ValueError("Missing speech recognition configuration in AI section")

        # Validate security configuration
        required_security = ['sound_threshold', 'motion_sensitivity', 'alert_cooldown']
        for param in required_security:
            if param not in self.config['security']:
                raise ValueError(f"Missing required security parameter: {param}")

        # Validate voice configuration
        if 'wake_word' not in self.config['voice']:
            raise ValueError("Missing wake word in voice configuration")

        # Validate logging configuration
        required_logging = ['level', 'file', 'max_size', 'backup_count']
        for param in required_logging:
            if param not in self.config['logging']:
                raise ValueError(f"Missing required logging parameter: {param}")

        # Validate storage configuration
        required_storage = ['voice_diary_path', 'models_path', 'cache_path']
        for param in required_storage:
            if param not in self.config['storage']:
                raise ValueError(f"Missing required storage parameter: {param}")

    def save_config(self, config: Dict[str, Any]):
        """
        Save configuration to file.
        
        Args:
            config (Dict[str, Any]): Configuration to save
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            raise

    def get_value(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section (str): Configuration section
            key (str): Configuration key
            default (Any): Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        try:
            return self.config[section][key]
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Configuration key not found: {section}.{key}")

    def set_value(self, section: str, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            section (str): Configuration section
            key (str): Configuration key
            value (Any): Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config(self.config) 