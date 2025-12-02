"""
小说转有声读物 - 主程序
提供完整的TXT转MP3功能
"""
import asyncio
from pathlib import Path
from typing import Optional
from loguru import logger

from modules.novel_reader import TextProcessor
from modules.tts_engine import EdgeTTSEngine, TTSConfig
from modules.audio_processor import AudioMerger, AudioPlayer
from core import ConfigManager, TaskManager


class NovelToAudio:
    """小说转有声读物转换器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化转换器

        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        self.config = ConfigManager(config_path)

        # 初始化文本处理器
        text_config = self.config.get_text_config()
        self.text_processor = TextProcessor(
            encoding=text_config.get('encoding'),
            remove_annotations=text_config.get('remove_annotations', True),
            remove_ads=text_config.get('remove_ads', True),
            max_segment_length=text_config.get('max_segment_length', 500)
        )

        # 初始化TTS引擎
        tts_config_data = self.config.get_tts_config()
        engine_type = tts_config_data.get('default_engine', 'edge-tts')

        if engine_type == 'edge-tts':
            edge_config = tts_config_data.get('edge', {})
            tts_config = TTSConfig(
                voice=edge_config.get('default_voice', 'zh-CN-XiaoxiaoNeural'),
                rate=edge_config.get('speech_rate', 1.0),
                volume=edge_config.get('volume', 1.0),
                pitch=edge_config.get('pitch', 1.0)
            )
            self.tts_engine = EdgeTTSEngine(tts_config)
        else:
            raise ValueError(f"不支持的TTS引擎: {engine_type}")

        # 初始化任务管理器
        perf_config = self.config.get('performance', {})
        self.task_manager = TaskManager(
            max_workers=perf_config.get('max_workers', 4)
        )

        # 初始化音频处理器
        audio_config = self.config.get_audio_config()
        self.audio_merger = AudioMerger(
            add_silence=True,
            silence_duration=audio_config.get('silence_between', 500)
        )

        logger.success("小说转有声读物系统初始化完成")

    def convert(
        self,
        novel_path: str,
        output_dir: Optional[str] = None,
        merge: bool = False,
        voice: Optional[str] = None
    ) -> dict:
        """
        转换小说为有声读物

        Args:
            novel_path: 小说文件路径
            output_dir: 输出目录（None则使用配置）
            merge: 是否合并所有章节
            voice: 指定音色（None则使用配置）

        Returns:
            转换结果
        """
        try:
            logger.info(f"=" * 60)
            logger.info(f"开始转换小说: {novel_path}")
            logger.info(f"=" * 60)

            # 1. 加载并处理小说
            logger.info("【步骤1/4】 加载并处理小说文本...")
            novel_data = self.text_processor.load_novel(novel_path)
            chapters = novel_data['chapters']

            logger.info(f"✓ 小说加载完成:")
            logger.info(f"  - 书名: {Path(novel_path).stem}")
            logger.info(f"  - 章节数: {len(chapters)}")
            logger.info(f"  - 总字数: {novel_data['summary']['total_characters']:,}")

            # 2. 准备TTS任务
            logger.info("\n【步骤2/4】 准备TTS合成任务...")
            tts_tasks = self.text_processor.prepare_for_tts(chapters)

            # 设置输出目录
            if output_dir is None:
                output_config = self.config.get_output_config()
                output_dir = output_config.get('base_dir', './data/output')

            output_path = Path(output_dir) / Path(novel_path).stem
            output_path.mkdir(parents=True, exist_ok=True)

            logger.info(f"✓ 任务准备完成:")
            logger.info(f"  - 任务数: {len(tts_tasks)}")
            logger.info(f"  - 输出目录: {output_path}")

            # 设置音色
            if voice:
                if hasattr(self.tts_engine, 'set_voice_by_name'):
                    self.tts_engine.set_voice_by_name(voice)
                else:
                    self.tts_engine.set_voice(voice)

            # 3. 批量合成音频
            logger.info("\n【步骤3/4】 批量合成音频...")
            self.task_manager.clear()

            # 添加任务
            for task in tts_tasks:
                output_file = output_path / f"{task['chapter_index']:03d}_{task['segment_index']:02d}.mp3"
                self.task_manager.add_task(
                    task_id=task['task_id'],
                    text=task['text'],
                    output_path=str(output_file),
                    chapter_title=task['chapter_title'],
                    metadata=task
                )

            # 执行合成
            result = self.task_manager.execute_sync(self.tts_engine, show_progress=True)

            logger.info(f"\n✓ 音频合成完成:")
            logger.info(f"  - 成功: {result['completed']}/{result['total']}")
            logger.info(f"  - 失败: {result['failed']}")

            # 4. 合并音频（如果需要）
            merged_file = None
            if merge and result['completed'] > 0:
                logger.info("\n【步骤4/4】 合并音频文件...")

                completed_tasks = self.task_manager.get_completed_tasks()
                audio_files = [task.output_path for task in completed_tasks]

                merged_file = output_path / f"{Path(novel_path).stem}_完整版.mp3"
                self.audio_merger.merge_files(audio_files, str(merged_file))

                logger.info(f"✓ 音频已合并: {merged_file}")
            else:
                logger.info("\n【步骤4/4】 跳过音频合并")

            # 返回结果
            return {
                'success': result['failed'] == 0,
                'novel_path': novel_path,
                'output_dir': str(output_path),
                'chapters': len(chapters),
                'tasks_total': result['total'],
                'tasks_completed': result['completed'],
                'tasks_failed': result['failed'],
                'merged_file': str(merged_file) if merged_file else None,
                'audio_files': [task.output_path for task in self.task_manager.get_completed_tasks()]
            }

        except Exception as e:
            logger.error(f"转换失败: {e}")
            raise

    def convert_chapter(
        self,
        chapter_text: str,
        chapter_title: str,
        output_path: str,
        voice: Optional[str] = None
    ) -> bool:
        """
        转换单个章节

        Args:
            chapter_text: 章节文本
            chapter_title: 章节标题
            output_path: 输出路径
            voice: 音色

        Returns:
            是否成功
        """
        try:
            if voice:
                if hasattr(self.tts_engine, 'set_voice_by_name'):
                    self.tts_engine.set_voice_by_name(voice)
                else:
                    self.tts_engine.set_voice(voice)

            logger.info(f"转换章节: {chapter_title}")
            success = self.tts_engine.synthesize_sync(chapter_text, output_path)

            if success:
                logger.success(f"✓ 章节转换成功: {output_path}")
            else:
                logger.error(f"✗ 章节转换失败")

            return success

        except Exception as e:
            logger.error(f"章节转换失败: {e}")
            return False

    def play_audio(self, audio_path: str, speed: float = 1.0):
        """
        播放音频

        Args:
            audio_path: 音频文件路径
            speed: 播放速度
        """
        player = AudioPlayer()

        if player.load(audio_path):
            player.set_speed(speed)
            player.play()

            logger.info("正在播放，按 Ctrl+C 停止...")

            try:
                import time
                while player.is_playing():
                    time.sleep(0.1)
            except KeyboardInterrupt:
                player.stop()
                logger.info("播放已停止")

            player.cleanup()

    def list_voices(self):
        """列出可用音色"""
        voices = self.tts_engine.get_available_voices()

        logger.info(f"\n可用音色列表 (共 {len(voices)} 个):")
        logger.info("=" * 60)

        for voice in voices:
            logger.info(f"  • {voice.name}")
            logger.info(f"    语言: {voice.language} | 性别: {voice.gender}")
            if voice.description:
                logger.info(f"    描述: {voice.description}")
            logger.info("")

        # 显示推荐音色
        if hasattr(self.tts_engine, 'RECOMMENDED_VOICES'):
            logger.info("\n推荐音色 (简称):")
            logger.info("=" * 60)
            for name, voice_id in self.tts_engine.RECOMMENDED_VOICES.items():
                logger.info(f"  • {name:12} -> {voice_id}")


if __name__ == '__main__':
    # 测试代码
    converter = NovelToAudio()

    # 示例1: 转换小说
    # result = converter.convert("test_novel.txt", merge=True, voice="xiaoxiao")
    # print(f"转换结果: {result}")

    # 示例2: 列出音色
    # converter.list_voices()

    # 示例3: 播放音频
    # converter.play_audio("output/test.mp3", speed=1.5)
