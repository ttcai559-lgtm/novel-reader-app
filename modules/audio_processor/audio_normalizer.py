"""
音频标准化处理器
支持音量标准化、降噪等处理
"""
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pathlib import Path
from loguru import logger


class AudioNormalizer:
    """音频标准化处理器"""

    @staticmethod
    def normalize_volume(audio_path: str, output_path: str = None) -> bool:
        """
        标准化音量

        Args:
            audio_path: 输入音频路径
            output_path: 输出路径（None则覆盖原文件）

        Returns:
            是否成功
        """
        try:
            # 加载音频
            audio = AudioSegment.from_file(audio_path)

            # 标准化
            normalized = normalize(audio)

            # 保存
            output_path = output_path or audio_path
            format = Path(output_path).suffix[1:]
            normalized.export(output_path, format=format)

            logger.success(f"音量标准化完成: {output_path}")
            return True

        except Exception as e:
            logger.error(f"音量标准化失败: {e}")
            return False

    @staticmethod
    def compress_dynamic(audio_path: str, output_path: str = None, threshold: float = -20.0) -> bool:
        """
        动态范围压缩

        Args:
            audio_path: 输入路径
            output_path: 输出路径
            threshold: 压缩阈值(dB)

        Returns:
            是否成功
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            compressed = compress_dynamic_range(audio, threshold=threshold)

            output_path = output_path or audio_path
            format = Path(output_path).suffix[1:]
            compressed.export(output_path, format=format)

            logger.success(f"动态压缩完成: {output_path}")
            return True

        except Exception as e:
            logger.error(f"动态压缩失败: {e}")
            return False

    @staticmethod
    def adjust_volume(audio_path: str, output_path: str, db_change: float) -> bool:
        """
        调整音量

        Args:
            audio_path: 输入路径
            output_path: 输出路径
            db_change: 音量变化(dB)

        Returns:
            是否成功
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            adjusted = audio + db_change

            format = Path(output_path).suffix[1:]
            adjusted.export(output_path, format=format)

            logger.success(f"音量调整完成: {output_path} ({db_change:+.1f}dB)")
            return True

        except Exception as e:
            logger.error(f"音量调整失败: {e}")
            return False
