"""
TTS引擎模块
"""
from .base_tts import BaseTTS, TTSConfig, VoiceInfo
from .local_tts.edge_tts_engine import EdgeTTSEngine

__all__ = ['BaseTTS', 'TTSConfig', 'VoiceInfo', 'EdgeTTSEngine']
