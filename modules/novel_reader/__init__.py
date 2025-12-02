"""
小说阅读器模块
"""
from .text_processor import TextProcessor
from .chapter_parser import ChapterParser
from .encoding_detector import EncodingDetector
from .text_cleaner import TextCleaner

__all__ = ['TextProcessor', 'ChapterParser', 'EncodingDetector', 'TextCleaner']
