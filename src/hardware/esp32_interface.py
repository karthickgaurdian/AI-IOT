"""
ESP32 Interface Module
Handles communication with ESP32 hardware components.
"""

import serial
import time
import json
import logging
from typing import Dict, Any

class ESP32Interface:
    def __init__(self, port: str, baud_rate: int = 115200):
        """
        Initialize ESP32 interface.
        
        Args:
            port (str): Serial port for ESP32 (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baud_rate (int): Serial communication baud rate
        """
        self.port = port
        self.baud_rate = baud_rate
        self.serial = None
        self.logger = logging.getLogger(__name__)
        self.connect()

    def connect(self):
        """Establish connection with ESP32."""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=1
            )
            time.sleep(2)  # Wait for ESP32 to reset
            self.logger.info(f"Connected to ESP32 on {self.port}")
        except serial.SerialException as e:
            self.logger.error(f"Failed to connect to ESP32: {e}")
            raise

    def send_command(self, command: str) -> bool:
        """
        Send command to ESP32.
        
        Args:
            command (str): Command to send
            
        Returns:
            bool: True if command was sent successfully
        """
        try:
            self.serial.write(f"{command}\n".encode())
            return True
        except serial.SerialException as e:
            self.logger.error(f"Failed to send command: {e}")
            return False

    def read_sensor_data(self) -> Dict[str, Any]:
        """
        Read sensor data from ESP32.
        
        Returns:
            Dict[str, Any]: Dictionary containing sensor readings
        """
        try:
            if self.serial.in_waiting:
                data = self.serial.readline().decode().strip()
                return json.loads(data)
            return {}
        except (json.JSONDecodeError, serial.SerialException) as e:
            self.logger.error(f"Failed to read sensor data: {e}")
            return {}

    def read_pir_sensor(self) -> float:
        """
        Read PIR motion sensor value.
        
        Returns:
            float: Motion sensor reading (0-1)
        """
        data = self.read_sensor_data()
        return data.get('pir', 0.0)

    def read_sound_level(self) -> float:
        """
        Read sound level from microphone.
        
        Returns:
            float: Sound level in decibels
        """
        data = self.read_sensor_data()
        return data.get('sound', 0.0)

    def read_temperature(self) -> float:
        """
        Read temperature sensor value.
        
        Returns:
            float: Temperature in Celsius
        """
        data = self.read_sensor_data()
        return data.get('temperature', 0.0)

    def set_led_color(self, r: int, g: int, b: int):
        """
        Set LED ring color.
        
        Args:
            r (int): Red component (0-255)
            g (int): Green component (0-255)
            b (int): Blue component (0-255)
        """
        command = f"LED {r} {g} {b}"
        self.send_command(command)

    def speak(self, text: str):
        """
        Convert text to speech and play through speaker.
        
        Args:
            text (str): Text to speak
        """
        command = f"SPEAK {text}"
        self.send_command(command)

    def close(self):
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.logger.info("Closed ESP32 connection") 