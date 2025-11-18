"""
Voice Interface for Autonomous UI Engine
Phase 6: Innovation

Speech-to-text, text-to-speech, and voice command processing.
"""

from .speech_to_text import SpeechToText, VoiceCommandRecognizer
from .text_to_speech import TextToSpeech, VoiceResponseGenerator
from .voice_commands import VoiceCommandProcessor, VoiceInterface

__all__ = [
    'SpeechToText',
    'VoiceCommandRecognizer',
    'TextToSpeech',
    'VoiceResponseGenerator',
    'VoiceCommandProcessor',
    'VoiceInterface',
]
