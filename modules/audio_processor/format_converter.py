"""
音频格式转换器
支持多种格式互转
"""
from pydub import AudioSegment
from pathlib import Path
from typing import Optional
from loguru import logger


class FormatConverter:
    """音频格式转换器"""

    SUPPORTED_FORMATS = ['mp3', 'wav', 'm4a', 'ogg', 'flac', 'aac']

    @staticmethod
    def convert(
        input_path: str,
        output_path: str,
        output_format: Optional[str] = None,
        bitrate: str = "192k",
        sample_rate: int = 44100
    ) -> bool:
        """
        转换音频格式

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            output_format: 输出格式（None则从文件扩展名推断）
            bitrate: 比特率
            sample_rate: 采样率

        Returns:
            是否成功
        """
        try:
            # 加载音频
            audio = AudioSegment.from_file(input_path)

            # 确定输出格式
            if output_format is None:
                output_format = Path(output_path).suffix[1:]

            if output_format not in FormatConverter.SUPPORTED_FORMATS:
                logger.warning(f"不支持的格式: {output_format}，使用mp3")
                output_format = 'mp3'

            # 设置采样率
            audio = audio.set_frame_rate(sample_rate)

            # 导出
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            audio.export(
                str(output_path),
                format=output_format,
                bitrate=bitrate
            )

            logger.success(f"格式转换完成: {input_path} -> {output_path}")
            return True

        except Exception as e:
            logger.error(f"格式转换失败: {e}")
            return False

    @staticmethod
    def batch_convert(
        input_files: list,
        output_dir: str,
        output_format: str = "mp3",
        bitrate: str = "192k"
    ) -> int:
        """
        批量转换

        Args:
            input_files: 输入文件列表
            output_dir: 输出目录
            output_format: 输出格式
            bitrate: 比特率

        Returns:
            成功转换的文件数
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0

        for input_file in input_files:
            input_path = Path(input_file)
            output_path = output_dir / f"{input_path.stem}.{output_format}"

            if FormatConverter.convert(str(input_path), str(output_path), output_format, bitrate):
                success_count += 1

        logger.info(f"批量转换完成: {success_count}/{len(input_files)} 成功")
        return success_count
