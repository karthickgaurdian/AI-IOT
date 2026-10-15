#!/usr/bin/env python3
"""
AI Companion Cube - Main Application
This is the main entry point for the AI Companion Cube application.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Import custom modules
from src.ai.speech_recognition import SpeechRecognizer
from src.ai.sentiment_analyzer import SentimentAnalyzer
from src.hardware.esp32_interface import ESP32Interface
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger

class CompanionCube:
    def __init__(self):
        """Initialize the AI Companion Cube."""
        # Load configuration
        self.config = ConfigLoader().load_config()
        
        # Setup logging
        self.logger = setup_logger(
            self.config['logging']['level'],
            self.config['logging']['file']
        )
        
        # Initialize components
        self.esp32 = ESP32Interface(
            port=self.config['hardware']['esp32']['port'],
            baud_rate=self.config['hardware']['esp32']['baud_rate']
        )
        
        self.speech_recognizer = SpeechRecognizer(
            language=self.config['ai']['speech_recognition']['language'],
            energy_threshold=self.config['ai']['speech_recognition']['energy_threshold']
        )
        
        self.sentiment_analyzer = SentimentAnalyzer(
            model_path=self.config['ai']['sentiment_analysis']['model_path']
        )
        
        self.logger.info("AI Companion Cube initialized successfully")

    def start(self):
        """Start the AI Companion Cube main loop."""
        self.logger.info("Starting AI Companion Cube...")
        
        try:
            while True:
                # Listen for wake word
                if self.speech_recognizer.detect_wake_word(self.config['voice']['wake_word']):
                    self.logger.info("Wake word detected!")
                    
                    # Process voice command
                    command = self.speech_recognizer.listen()
                    if command:
                        self.process_command(command)
                
                # Check security sensors
                self.check_security()
                
                # Monitor health
                self.monitor_health()
                
        except KeyboardInterrupt:
            self.logger.info("Shutting down AI Companion Cube...")
            self.cleanup()

    def process_command(self, command):
        """Process voice commands and execute appropriate actions."""
        self.logger.info(f"Processing command: {command}")
        
        # Analyze sentiment
        sentiment = self.sentiment_analyzer.analyze(command)
        
        # Execute command based on intent
        if "reminder" in command.lower():
            self.set_reminder(command)
        elif "health" in command.lower():
            self.provide_health_advice()
        elif "diary" in command.lower():
            self.record_diary_entry(command)
        else:
            self.respond_to_general_query(command)

    def check_security(self):
        """Monitor security sensors and trigger alerts if needed."""
        # Check PIR sensor
        if self.esp32.read_pir_sensor() > self.config['security']['motion_sensitivity']:
            self.trigger_security_alert("motion")
        
        # Check sound levels
        if self.esp32.read_sound_level() > self.config['security']['sound_threshold']:
            self.trigger_security_alert("sound")

    def monitor_health(self):
        """Monitor health metrics and provide reminders."""
        current_time = datetime.now().strftime("%H:%M")
        
        # Check hydration reminder
        if self.should_remind_hydration():
            self.esp32.speak("Time to drink some water!")
        
        # Check sleep reminder
        if current_time == self.config['ai']['health_monitoring']['sleep_reminder_time']:
            self.esp32.speak("It's time to prepare for bed!")

    def cleanup(self):
        """Clean up resources before shutting down."""
        self.esp32.close()
        self.logger.info("Cleanup completed")

def main():
    """Main entry point for the application."""
    companion = CompanionCube()
    companion.start()

if __name__ == "__main__":
    main() 