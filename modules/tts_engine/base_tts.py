"""
TTS引擎基类
定义统一的TTS接口
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict
from pathlib import Path


@dataclass
class VoiceInfo:
    """音色信息"""
    name: str  # 音色名称
    language: str  # 语言代码
    gender: str  # 性别: Male/Female
    description: str = ""  # 描述


@dataclass
class TTSConfig:
    """TTS配置"""
    voice: str  # 音色名称
    rate: float = 1.0  # 语速 (0.5 - 2.0)
    volume: float = 1.0  # 音量 (0.0 - 1.0)
    pitch: float = 1.0  # 音调 (0.5 - 2.0)
    output_format: str = "mp3"  # 输出格式


class BaseTTS(ABC):
    """TTS引擎基类"""

    def __init__(self, config: Optional[TTSConfig] = None):
        """
        初始化TTS引擎

        Args:
            config: TTS配置
        """
        self.config = config or TTSConfig(voice="default")

    @abstractmethod
    async def synthesize(self, text: str, output_path: str) -> bool:
        """
        合成语音（异步）

        Args:
            text: 要合成的文本
            output_path: 输出文件路径

        Returns:
            是否成功
        """
        pass

    def synthesize_sync(self, text: str, output_path: str) -> bool:
        """
        合成语音（同步）

        Args:
            text: 要合成的文本
            output_path: 输出文件路径

        Returns:
            是否成功
        """
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.synthesize(text, output_path))

    @abstractmethod
    def get_available_voices(self) -> List[VoiceInfo]:
        """
        获取可用的音色列表

        Returns:
            音色信息列表
        """
        pass

    @abstractmethod
    def get_engine_name(self) -> str:
        """
        获取引擎名称

        Returns:
            引擎名称
        """
        pass

    def validate_config(self) -> bool:
        """
        验证配置是否有效

        Returns:
            配置是否有效
        """
        if not 0.5 <= self.config.rate <= 2.0:
            return False
        if not 0.0 <= self.config.volume <= 1.0:
            return False
        if not 0.5 <= self.config.pitch <= 2.0:
            return False
        return True

    def set_voice(self, voice: str):
        """设置音色"""
        self.config.voice = voice

    def set_rate(self, rate: float):
        """设置语速"""
        self.config.rate = max(0.5, min(2.0, rate))

    def set_volume(self, volume: float):
        """设置音量"""
        self.config.volume = max(0.0, min(1.0, volume))

    def set_pitch(self, pitch: float):
        """设置音调"""
        self.config.pitch = max(0.5, min(2.0, pitch))

    def get_info(self) -> Dict:
        """
        获取引擎信息

        Returns:
            引擎信息字典
        """
        return {
            'name': self.get_engine_name(),
            'config': {
                'voice': self.config.voice,
                'rate': self.config.rate,
                'volume': self.config.volume,
                'pitch': self.config.pitch,
                'output_format': self.config.output_format
            },
            'available_voices': len(self.get_available_voices())
        }
