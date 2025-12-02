"""
Microsoft Edge TTS引擎
基于edge-tts库，提供高质量免费TTS服务
"""
import edge_tts
from typing import List, Optional
from pathlib import Path
from loguru import logger

from ..base_tts import BaseTTS, TTSConfig, VoiceInfo


class EdgeTTSEngine(BaseTTS):
    """Microsoft Edge TTS引擎"""

    # 推荐的中文音色
    RECOMMENDED_VOICES = {
        # 女声
        'xiaoxiao': 'zh-CN-XiaoxiaoNeural',  # 晓晓 - 温柔女声
        'xiaoyi': 'zh-CN-XiaoyiNeural',      # 晓伊 - 甜美女声
        'xiaomeng': 'zh-CN-XiaomengNeural',  # 晓梦 - 少女音
        'xiaoyan': 'zh-CN-XiaoyanNeural',    # 晓颜 - 成熟女声

        # 男声
        'yunxi': 'zh-CN-YunxiNeural',        # 云希 - 青年男声
        'yunyang': 'zh-CN-YunyangNeural',    # 云扬 - 磁性男声
        'yunjian': 'zh-CN-YunjianNeural',    # 云健 - 沉稳男声

        # 特色
        'yunxia': 'zh-CN-YunxiaNeural',      # 云夏 - 播音腔
    }

    def __init__(self, config: Optional[TTSConfig] = None):
        """
        初始化Edge TTS引擎

        Args:
            config: TTS配置
        """
        if config is None:
            config = TTSConfig(voice=self.RECOMMENDED_VOICES['xiaoxiao'])

        super().__init__(config)
        self._voices_cache = None
        logger.info(f"Edge TTS引擎初始化完成，当前音色: {self.config.voice}")

    async def synthesize(self, text: str, output_path: str) -> bool:
        """
        合成语音

        Args:
            text: 要合成的文本
            output_path: 输出文件路径

        Returns:
            是否成功
        """
        try:
            # 确保输出目录存在
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # 计算语速（edge-tts使用百分比）
            rate_str = self._calculate_rate(self.config.rate)
            volume_str = self._calculate_volume(self.config.volume)
            pitch_str = self._calculate_pitch(self.config.pitch)

            logger.info(f"开始合成: {len(text)} 字符")
            logger.debug(f"参数 - 音色: {self.config.voice}, 语速: {rate_str}, 音量: {volume_str}, 音调: {pitch_str}")

            # 创建TTS通信对象
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.config.voice,
                rate=rate_str,
                volume=volume_str,
                pitch=pitch_str
            )

            # 保存音频文件
            await communicate.save(str(output_file))

            logger.success(f"音频合成成功: {output_file}")
            return True

        except Exception as e:
            logger.error(f"音频合成失败: {e}")
            return False

    def get_available_voices(self) -> List[VoiceInfo]:
        """
        获取可用的音色列表

        Returns:
            音色信息列表
        """
        if self._voices_cache is not None:
            return self._voices_cache

        try:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            voices = loop.run_until_complete(edge_tts.list_voices())

            # 只返回中文音色
            voice_list = []
            for voice in voices:
                if voice['Locale'].startswith('zh'):
                    voice_list.append(VoiceInfo(
                        name=voice['ShortName'],
                        language=voice['Locale'],
                        gender=voice['Gender'],
                        description=voice.get('FriendlyName', '')
                    ))

            self._voices_cache = voice_list
            logger.info(f"获取到 {len(voice_list)} 个中文音色")
            return voice_list

        except Exception as e:
            logger.error(f"获取音色列表失败: {e}")
            return []

    def get_engine_name(self) -> str:
        """获取引擎名称"""
        return "Microsoft Edge TTS"

    def get_recommended_voices(self) -> dict:
        """
        获取推荐的音色映射

        Returns:
            音色映射字典
        """
        return self.RECOMMENDED_VOICES

    def set_voice_by_name(self, name: str):
        """
        通过简短名称设置音色

        Args:
            name: 音色简称（如 'xiaoxiao', 'yunxi'）
        """
        if name in self.RECOMMENDED_VOICES:
            self.config.voice = self.RECOMMENDED_VOICES[name]
            logger.info(f"音色已设置为: {name} ({self.config.voice})")
        else:
            logger.warning(f"未找到音色: {name}，使用完整ID设置")
            self.config.voice = name

    @staticmethod
    def _calculate_rate(rate: float) -> str:
        """
        计算语速参数

        Args:
            rate: 语速倍数 (0.5 - 2.0)

        Returns:
            edge-tts格式的语速字符串
        """
        # edge-tts使用 +X% 或 -X% 格式
        # 1.0 对应 +0%, 1.5 对应 +50%, 0.5 对应 -50%
        percentage = int((rate - 1.0) * 100)
        if percentage >= 0:
            return f"+{percentage}%"
        else:
            return f"{percentage}%"

    @staticmethod
    def _calculate_volume(volume: float) -> str:
        """
        计算音量参数

        Args:
            volume: 音量 (0.0 - 1.0)

        Returns:
            edge-tts格式的音量字符串
        """
        # 转换为百分比 (0-100%)
        percentage = int((volume - 1.0) * 100)
        if percentage >= 0:
            return f"+{percentage}%"
        else:
            return f"{percentage}%"

    @staticmethod
    def _calculate_pitch(pitch: float) -> str:
        """
        计算音调参数

        Args:
            pitch: 音调倍数 (0.5 - 2.0)

        Returns:
            edge-tts格式的音调字符串
        """
        # edge-tts使用Hz或相对值
        # 这里使用相对百分比
        percentage = int((pitch - 1.0) * 50)  # 减小变化幅度
        if percentage >= 0:
            return f"+{percentage}Hz"
        else:
            return f"{percentage}Hz"


if __name__ == '__main__':
    # 测试代码
    import asyncio

    async def test_edge_tts():
        # 初始化引擎
        config = TTSConfig(
            voice='zh-CN-XiaoxiaoNeural',
            rate=1.0,
            volume=1.0
        )
        engine = EdgeTTSEngine(config)

        # 测试文本
        test_text = "你好，这是一个测试。我是晓晓，很高兴为你朗读小说。"

        # 合成音频
        output_path = "test_output.mp3"
        success = await engine.synthesize(test_text, output_path)

        if success:
            print(f"✓ 合成成功: {output_path}")
        else:
            print("✗ 合成失败")

        # 获取音色列表
        voices = engine.get_available_voices()
        print(f"\n可用音色数量: {len(voices)}")
        print("推荐音色:")
        for name, voice_id in engine.RECOMMENDED_VOICES.items():
            print(f"  - {name}: {voice_id}")

    # 运行测试
    # asyncio.run(test_edge_tts())
