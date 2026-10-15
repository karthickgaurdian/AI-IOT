"""
Sentiment Analyzer Module
Analyzes text sentiment and detects user mood.
"""

import numpy as np
import tensorflow as tf
from transformers import pipeline
import logging
from typing import Dict, Any, Tuple
import json
import os

class SentimentAnalyzer:
    def __init__(self, model_path: str = None):
        """
        Initialize sentiment analyzer.
        
        Args:
            model_path (str): Path to pre-trained model
        """
        self.logger = logging.getLogger(__name__)
        
        # Load pre-trained sentiment analysis model
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=0 if tf.config.list_physical_devices('GPU') else -1
            )
            self.logger.info("Sentiment analyzer initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize sentiment analyzer: {e}")
            raise

        # Load emotion keywords
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful'],
            'sad': ['sad', 'depressed', 'unhappy', 'miserable', 'down'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'irritated'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil']
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text sentiment and detect emotions.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, Any]: Analysis results including sentiment and emotions
        """
        try:
            # Get base sentiment
            sentiment_result = self.sentiment_analyzer(text)[0]
            
            # Detect emotions
            emotions = self._detect_emotions(text)
            
            # Calculate confidence scores
            confidence = {
                'sentiment': sentiment_result['score'],
                'emotions': {emotion: score for emotion, score in emotions}
            }
            
            return {
                'sentiment': sentiment_result['label'],
                'emotions': emotions,
                'confidence': confidence,
                'text': text
            }
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {e}")
            return {
                'sentiment': 'NEUTRAL',
                'emotions': [],
                'confidence': {'sentiment': 0.0, 'emotions': {}},
                'text': text
            }

    def _detect_emotions(self, text: str) -> list:
        """
        Detect emotions in text using keyword matching.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list: List of (emotion, score) tuples
        """
        text = text.lower()
        emotions = []
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                emotions.append((emotion, score / len(keywords)))
        
        return sorted(emotions, key=lambda x: x[1], reverse=True)

    def get_mood_summary(self, text: str) -> str:
        """
        Get a human-readable mood summary.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Mood summary
        """
        analysis = self.analyze(text)
        
        # Get primary emotion
        primary_emotion = analysis['emotions'][0][0] if analysis['emotions'] else 'neutral'
        
        # Generate summary
        if analysis['sentiment'] == 'POSITIVE':
            if primary_emotion == 'happy':
                return "You seem to be in a good mood!"
            elif primary_emotion == 'calm':
                return "You appear to be feeling peaceful and relaxed."
        elif analysis['sentiment'] == 'NEGATIVE':
            if primary_emotion == 'sad':
                return "You seem to be feeling down. Would you like to talk about it?"
            elif primary_emotion == 'anxious':
                return "You appear to be feeling anxious. Would you like some calming advice?"
            elif primary_emotion == 'angry':
                return "You seem to be feeling frustrated. Would you like to take a moment to breathe?"
        
        return "I'm here if you need someone to talk to."

    def save_analysis(self, analysis: Dict[str, Any], filepath: str):
        """
        Save sentiment analysis results to file.
        
        Args:
            analysis (Dict[str, Any]): Analysis results
            filepath (str): Path to save results
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(analysis, f, indent=2)
            self.logger.info(f"Analysis saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save analysis: {e}")

    def load_analysis(self, filepath: str) -> Dict[str, Any]:
        """
        Load sentiment analysis results from file.
        
        Args:
            filepath (str): Path to load results from
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load analysis: {e}")
            return {} 