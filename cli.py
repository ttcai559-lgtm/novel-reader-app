#!/usr/bin/env python
"""
APP_Tool 命令行工具
提供命令行界面访问小说转有声读物功能
"""
import click
from pathlib import Path
from loguru import logger
import sys

from novel_to_audio import NovelToAudio


# 配置日志
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:8}</level> | <level>{message}</level>",
    level="INFO"
)


@click.group()
@click.version_option(version="1.0.0", prog_name="APP_Tool")
def cli():
    """
    APP_Tool - TXT小说转有声读物工具

    \b
    示例:
        # 转换小说
        python cli.py convert novel.txt

        # 使用指定音色
        python cli.py convert novel.txt --voice xiaoxiao

        # 转换并合并所有章节
        python cli.py convert novel.txt --merge

        # 列出可用音色
        python cli.py voices

        # 播放音频
        python cli.py play output/chapter1.mp3 --speed 1.5
    """
    pass


@cli.command()
@click.argument('novel_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='输出目录', type=click.Path())
@click.option('--voice', '-v', help='音色选择 (xiaoxiao, yunxi, xiaoyi等)')
@click.option('--merge/--no-merge', default=False, help='是否合并所有章节为单个文件')
@click.option('--config', '-c', help='配置文件路径', type=click.Path())
def convert(novel_path, output, voice, merge, config):
    """
    转换TXT小说为MP3有声读物

    \b
    NOVEL_PATH: 小说文件路径 (.txt)

    \b
    示例:
        python cli.py convert "三体.txt" -v xiaoxiao --merge
        python cli.py convert "novel.txt" -o ./output
    """
    try:
        click.echo("=" * 60)
        click.echo("  📚 APP_Tool - 小说转有声读物")
        click.echo("=" * 60)

        # 初始化转换器
        converter = NovelToAudio(config_path=config)

        # 执行转换
        result = converter.convert(
            novel_path=novel_path,
            output_dir=output,
            merge=merge,
            voice=voice
        )

        # 显示结果
        click.echo("\n" + "=" * 60)
        click.echo("  ✅ 转换完成!")
        click.echo("=" * 60)
        click.echo(f"📁 输出目录: {result['output_dir']}")
        click.echo(f"📊 统计:")
        click.echo(f"   - 章节数: {result['chapters']}")
        click.echo(f"   - 音频文件: {result['tasks_completed']}/{result['tasks_total']}")

        if result['merged_file']:
            click.echo(f"🎵 合并文件: {result['merged_file']}")

        if result['tasks_failed'] > 0:
            click.echo(f"⚠️  失败: {result['tasks_failed']} 个任务", err=True)

    except Exception as e:
        click.echo(f"❌ 转换失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', help='配置文件路径', type=click.Path())
def voices(config):
    """
    列出所有可用的TTS音色

    \b
    示例:
        python cli.py voices
    """
    try:
        converter = NovelToAudio(config_path=config)
        converter.list_voices()

    except Exception as e:
        click.echo(f"❌ 获取音色列表失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('audio_path', type=click.Path(exists=True))
@click.option('--speed', '-s', default=1.0, type=float, help='播放速度 (0.5-2.0)')
@click.option('--volume', '-v', default=0.8, type=float, help='音量 (0.0-1.0)')
def play(audio_path, speed, volume):
    """
    播放音频文件

    \b
    AUDIO_PATH: 音频文件路径

    \b
    示例:
        python cli.py play output/chapter1.mp3
        python cli.py play output/chapter1.mp3 --speed 1.5
    """
    try:
        from modules.audio_processor import AudioPlayer

        click.echo(f"🎵 播放: {audio_path}")
        click.echo(f"   速度: {speed}x | 音量: {volume:.0%}")
        click.echo("\n按 Ctrl+C 停止播放...\n")

        player = AudioPlayer()
        player.load(audio_path)
        player.set_speed(speed)
        player.set_volume(volume)
        player.play()

        import time
        while player.is_playing():
            time.sleep(0.1)

        player.cleanup()
        click.echo("\n✅ 播放结束")

    except KeyboardInterrupt:
        click.echo("\n⏹️  播放已停止")
    except Exception as e:
        click.echo(f"❌ 播放失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('chapter_text', type=str)
@click.argument('output_path', type=click.Path())
@click.option('--voice', '-v', help='音色选择')
@click.option('--title', '-t', help='章节标题', default="测试章节")
@click.option('--config', '-c', help='配置文件路径', type=click.Path())
def test(chapter_text, output_path, voice, title, config):
    """
    快速测试TTS合成

    \b
    CHAPTER_TEXT: 要合成的文本
    OUTPUT_PATH: 输出音频文件路径

    \b
    示例:
        python cli.py test "你好,这是一个测试" test.mp3 -v xiaoxiao
    """
    try:
        click.echo(f"🧪 测试TTS合成...")
        click.echo(f"   文本: {chapter_text[:50]}...")
        click.echo(f"   输出: {output_path}")

        converter = NovelToAudio(config_path=config)
        success = converter.convert_chapter(
            chapter_text=chapter_text,
            chapter_title=title,
            output_path=output_path,
            voice=voice
        )

        if success:
            click.echo(f"\n✅ 测试成功! 音频已保存到: {output_path}")
        else:
            click.echo(f"\n❌ 测试失败", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"❌ 测试失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('audio_files', nargs=-1, type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('--silence', '-s', default=500, type=int, help='章节间静音时长(毫秒)')
def merge(audio_files, output_path, silence):
    """
    合并多个音频文件

    \b
    AUDIO_FILES: 要合并的音频文件列表
    OUTPUT_PATH: 输出文件路径

    \b
    示例:
        python cli.py merge ch1.mp3 ch2.mp3 ch3.mp3 full.mp3
        python cli.py merge *.mp3 full.mp3 --silence 1000
    """
    try:
        from modules.audio_processor import AudioMerger

        if len(audio_files) < 2:
            click.echo("❌ 至少需要2个音频文件", err=True)
            sys.exit(1)

        click.echo(f"🔗 合并 {len(audio_files)} 个音频文件...")

        merger = AudioMerger(add_silence=True, silence_duration=silence)
        success = merger.merge_files(
            audio_files=list(audio_files),
            output_path=output_path
        )

        if success:
            click.echo(f"\n✅ 合并成功: {output_path}")
        else:
            click.echo(f"\n❌ 合并失败", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"❌ 合并失败: {e}", err=True)
        sys.exit(1)


@cli.command()
def config_show():
    """
    显示当前配置

    \b
    示例:
        python cli.py config-show
    """
    try:
        from core import ConfigManager

        config = ConfigManager()
        click.echo("📋 当前配置:")
        click.echo("=" * 60)
        click.echo(str(config))

    except Exception as e:
        click.echo(f"❌ 读取配置失败: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
