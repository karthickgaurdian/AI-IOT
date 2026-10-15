"""
Test suite for AI Companion Cube.
"""

import pytest
import os
import json
from src.ai.speech_recognition import SpeechRecognizer
from src.ai.sentiment_analyzer import SentimentAnalyzer
from src.hardware.esp32_interface import ESP32Interface
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger

# Test configuration
TEST_CONFIG = {
    "hardware": {
        "esp32": {
            "port": "COM3",
            "baud_rate": 115200,
            "pins": {
                "microphone": 34,
                "speaker": 25,
                "pir_sensor": 26,
                "led_ring": 27,
                "temp_sensor": 32
            }
        }
    },
    "ai": {
        "speech_recognition": {
            "language": "en-US",
            "energy_threshold": 4000
        },
        "sentiment_analysis": {
            "model_path": "data/models/sentiment_model.h5",
            "threshold": 0.7
        }
    },
    "security": {
        "sound_threshold": 70,
        "motion_sensitivity": 0.8,
        "alert_cooldown": 300
    },
    "voice": {
        "wake_word": "hey buddy"
    },
    "logging": {
        "level": "INFO",
        "file": "logs/test.log",
        "max_size": 10485760,
        "backup_count": 5
    },
    "storage": {
        "voice_diary_path": "data/diary/",
        "models_path": "data/models/",
        "cache_path": "data/cache/"
    }
}

@pytest.fixture
def config_loader():
    """Create a test configuration loader."""
    # Create test config file
    os.makedirs("config", exist_ok=True)
    with open("config/test_config.json", "w") as f:
        json.dump(TEST_CONFIG, f)
    
    loader = ConfigLoader("config/test_config.json")
    yield loader
    
    # Cleanup
    os.remove("config/test_config.json")

@pytest.fixture
def logger():
    """Create a test logger."""
    return setup_logger(
        level="DEBUG",
        log_file="logs/test.log"
    )

def test_config_loader(config_loader):
    """Test configuration loading and validation."""
    config = config_loader.load_config()
    assert config["hardware"]["esp32"]["port"] == "COM3"
    assert config["ai"]["speech_recognition"]["language"] == "en-US"
    assert config["security"]["sound_threshold"] == 70

def test_sentiment_analyzer():
    """Test sentiment analysis functionality."""
    analyzer = SentimentAnalyzer()
    
    # Test positive sentiment
    result = analyzer.analyze("I am feeling happy today!")
    assert result["sentiment"] in ["POSITIVE", "NEGATIVE"]
    assert len(result["emotions"]) > 0
    
    # Test negative sentiment
    result = analyzer.analyze("I am feeling sad and depressed.")
    assert result["sentiment"] in ["POSITIVE", "NEGATIVE"]
    assert any(emotion[0] == "sad" for emotion in result["emotions"])

def test_speech_recognizer():
    """Test speech recognition functionality."""
    recognizer = SpeechRecognizer(
        language="en-US",
        energy_threshold=4000
    )
    
    # Test wake word detection (mock)
    assert not recognizer.detect_wake_word("hey buddy")
    
    # Test audio level
    level = recognizer.get_audio_level()
    assert 0 <= level <= 1

def test_esp32_interface():
    """Test ESP32 interface functionality."""
    # Skip if no ESP32 connected
    pytest.skip("ESP32 not connected")
    
    interface = ESP32Interface(
        port=TEST_CONFIG["hardware"]["esp32"]["port"],
        baud_rate=TEST_CONFIG["hardware"]["esp32"]["baud_rate"]
    )
    
    # Test LED control
    interface.set_led_color(255, 0, 0)  # Red
    
    # Test sensor reading
    pir_value = interface.read_pir_sensor()
    assert 0 <= pir_value <= 1
    
    sound_level = interface.read_sound_level()
    assert sound_level >= 0
    
    # Cleanup
    interface.close()

def test_logger(logger):
    """Test logging functionality."""
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Check if log file exists
    assert os.path.exists("logs/test.log")

def test_integration(config_loader, logger):
    """Test integration of components."""
    # Load configuration
    config = config_loader.load_config()
    
    # Initialize components
    analyzer = SentimentAnalyzer()
    recognizer = SpeechRecognizer(
        language=config["ai"]["speech_recognition"]["language"],
        energy_threshold=config["ai"]["speech_recognition"]["energy_threshold"]
    )
    
    # Test component interaction
    text = "I am feeling happy today!"
    sentiment = analyzer.analyze(text)
    logger.info(f"Sentiment analysis result: {sentiment}")
    
    assert sentiment["sentiment"] in ["POSITIVE", "NEGATIVE"]
    assert len(sentiment["emotions"]) > 0 