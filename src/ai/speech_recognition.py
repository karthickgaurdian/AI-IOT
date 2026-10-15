"""
Speech Recognition Module
Handles voice command processing and wake word detection.
"""

import speech_recognition as sr
import numpy as np
import logging
from typing import Optional, Tuple
import threading
import queue
import time

class SpeechRecognizer:
    def __init__(self, language: str = "en-US", energy_threshold: int = 4000):
        """
        Initialize speech recognizer.
        
        Args:
            language (str): Language for speech recognition
            energy_threshold (int): Energy threshold for voice detection
        """
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.language = language
        self.logger = logging.getLogger(__name__)
        
        # Initialize microphone
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            self.logger.info("Microphone initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize microphone: {e}")
            raise

    def detect_wake_word(self, wake_word: str) -> bool:
        """
        Listen for wake word.
        
        Args:
            wake_word (str): Wake word to detect
            
        Returns:
            bool: True if wake word detected
        """
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
                text = self.recognizer.recognize_google(audio, language=self.language)
                return wake_word.lower() in text.lower()
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except Exception as e:
            self.logger.error(f"Error in wake word detection: {e}")
            return False

    def listen(self) -> Optional[str]:
        """
        Listen for voice command.
        
        Returns:
            Optional[str]: Recognized text or None if failed
        """
        try:
            with self.microphone as source:
                self.logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language=self.language)
                self.logger.info(f"Recognized: {text}")
                return text
        except sr.WaitTimeoutError:
            self.logger.warning("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
            return None
        except Exception as e:
            self.logger.error(f"Error in speech recognition: {e}")
            return None

    def continuous_listen(self, callback):
        """
        Continuously listen for voice commands in a separate thread.
        
        Args:
            callback: Function to call with recognized text
        """
        def listen_thread():
            while True:
                text = self.listen()
                if text:
                    callback(text)
                time.sleep(0.1)

        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()

    def adjust_for_noise(self):
        """Adjust recognizer for ambient noise."""
        try:
            with self.microphone as source:
                self.logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.logger.info("Ambient noise adjustment complete")
        except Exception as e:
            self.logger.error(f"Failed to adjust for ambient noise: {e}")

    def get_audio_level(self) -> float:
        """
        Get current audio level.
        
        Returns:
            float: Current audio level (0-1)
        """
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=0.1)
                return np.max(np.abs(audio.get_raw_data())) / 32768.0
        except:
            return 0.0 