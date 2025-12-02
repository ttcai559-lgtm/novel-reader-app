"""
音频合并器
支持合并多个音频文件为单个文件
"""
from pydub import AudioSegment
from pathlib import Path
from typing import List, Optional
from loguru import logger
from tqdm import tqdm


class AudioMerger:
    """音频合并器"""

    def __init__(self, add_silence: bool = True, silence_duration: int = 500):
        """
        初始化音频合并器

        Args:
            add_silence: 是否在音频间添加静音
            silence_duration: 静音时长(毫秒)
        """
        self.add_silence = add_silence
        self.silence_duration = silence_duration
        logger.info(f"音频合并器初始化 (静音间隔: {silence_duration}ms)")

    def merge_files(
        self,
        audio_files: List[str],
        output_path: str,
        format: str = "mp3",
        show_progress: bool = True
    ) -> bool:
        """
        合并多个音频文件

        Args:
            audio_files: 音频文件路径列表
            output_path: 输出文件路径
            format: 输出格式
            show_progress: 是否显示进度条

        Returns:
            是否成功
        """
        try:
            if not audio_files:
                logger.error("没有要合并的音频文件")
                return False

            logger.info(f"开始合并 {len(audio_files)} 个音频文件")

            # 初始化合并音频
            combined = AudioSegment.empty()

            # 创建静音片段
            silence = AudioSegment.silent(duration=self.silence_duration) if self.add_silence else None

            # 合并音频
            iterator = tqdm(audio_files, desc="合并音频") if show_progress else audio_files

            for i, audio_file in enumerate(iterator):
                if not Path(audio_file).exists():
                    logger.warning(f"文件不存在，跳过: {audio_file}")
                    continue

                # 加载音频
                audio = AudioSegment.from_file(audio_file)

                # 添加到合并音频
                combined += audio

                # 添加静音（除了最后一个）
                if silence and i < len(audio_files) - 1:
                    combined += silence

            # 导出
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            combined.export(str(output_path), format=format)

            duration = len(combined) / 1000.0
            logger.success(f"音频合并完成: {output_path} (时长: {duration:.1f}秒)")
            return True

        except Exception as e:
            logger.error(f"音频合并失败: {e}")
            return False

    def merge_chapters(
        self,
        chapter_audios: List[dict],
        output_path: str,
        format: str = "mp3"
    ) -> bool:
        """
        合并章节音频

        Args:
            chapter_audios: 章节音频列表 [{file, title}, ...]
            output_path: 输出路径
            format: 输出格式

        Returns:
            是否成功
        """
        audio_files = [ch['file'] for ch in chapter_audios]
        return self.merge_files(audio_files, output_path, format=format)


if __name__ == '__main__':
    # 测试代码
    merger = AudioMerger(add_silence=True, silence_duration=1000)

    # 示例：合并音频
    # files = ["chapter1.mp3", "chapter2.mp3", "chapter3.mp3"]
    # merger.merge_files(files, "full_audiobook.mp3")
