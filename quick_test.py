#!/usr/bin/env python
"""
快速测试脚本
验证系统是否正常工作
"""
import sys
from pathlib import Path

print("=" * 60)
print("  APP_Tool 快速测试")
print("=" * 60)

# 测试1: 检查依赖
print("\n【测试1】 检查依赖...")
try:
    import edge_tts
    print("✓ edge-tts: OK")
except ImportError:
    print("✗ edge-tts: 未安装 - 请运行: pip install edge-tts")
    sys.exit(1)

try:
    from pydub import AudioSegment
    print("✓ pydub: OK")
except ImportError:
    print("✗ pydub: 未安装 - 请运行: pip install pydub")
    sys.exit(1)

try:
    import pygame
    print("✓ pygame: OK")
except ImportError:
    print("✗ pygame: 未安装 - 请运行: pip install pygame")
    sys.exit(1)

try:
    import click
    print("✓ click: OK")
except ImportError:
    print("✗ click: 未安装 - 请运行: pip install click")
    sys.exit(1)

try:
    import chardet
    print("✓ chardet: OK")
except ImportError:
    print("✗ chardet: 未安装 - 请运行: pip install chardet")
    sys.exit(1)

try:
    from loguru import logger
    print("✓ loguru: OK")
except ImportError:
    print("✗ loguru: 未安装 - 请运行: pip install loguru")
    sys.exit(1)

try:
    import yaml
    print("✓ PyYAML: OK")
except ImportError:
    print("✗ PyYAML: 未安装 - 请运行: pip install PyYAML")
    sys.exit(1)

# 测试2: 检查模块导入
print("\n【测试2】 检查模块导入...")
try:
    from modules.novel_reader import TextProcessor
    print("✓ TextProcessor: OK")
except ImportError as e:
    print(f"✗ TextProcessor: 导入失败 - {e}")
    sys.exit(1)

try:
    from modules.tts_engine import EdgeTTSEngine, TTSConfig
    print("✓ EdgeTTSEngine: OK")
except ImportError as e:
    print(f"✗ EdgeTTSEngine: 导入失败 - {e}")
    sys.exit(1)

try:
    from core import ConfigManager, TaskManager
    print("✓ ConfigManager: OK")
    print("✓ TaskManager: OK")
except ImportError as e:
    print(f"✗ Core modules: 导入失败 - {e}")
    sys.exit(1)

try:
    from novel_to_audio import NovelToAudio
    print("✓ NovelToAudio: OK")
except ImportError as e:
    print(f"✗ NovelToAudio: 导入失败 - {e}")
    sys.exit(1)

# 测试3: 测试TTS引擎
print("\n【测试3】 测试TTS引擎...")
try:
    import asyncio

    async def test_tts():
        config = TTSConfig(voice='zh-CN-XiaoxiaoNeural')
        engine = EdgeTTSEngine(config)

        # 测试文本
        test_text = "你好,这是APP_Tool的测试。"
        output_path = "data/output/quick_test.mp3"

        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        print(f"  正在合成测试音频...")
        success = await engine.synthesize(test_text, output_path)

        if success and Path(output_path).exists():
            print(f"✓ TTS合成成功: {output_path}")
            return True
        else:
            print("✗ TTS合成失败")
            return False

    # 运行测试
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if not loop.run_until_complete(test_tts()):
        sys.exit(1)

except Exception as e:
    print(f"✗ TTS测试失败: {e}")
    print("  提示: 请检查网络连接(Edge TTS需要联网)")
    sys.exit(1)

# 测试4: 测试文本处理
print("\n【测试4】 测试文本处理...")
try:
    processor = TextProcessor()

    # 测试章节识别
    test_text = """
第一章 开始

这是第一章的内容。

第二章 继续

这是第二章的内容。
"""

    from modules.novel_reader import ChapterParser
    parser = ChapterParser()
    chapters = parser.parse(test_text)

    if len(chapters) >= 2:
        print(f"✓ 章节识别成功: 找到 {len(chapters)} 个章节")
    else:
        print(f"⚠ 章节识别: 只找到 {len(chapters)} 个章节")

except Exception as e:
    print(f"✗ 文本处理测试失败: {e}")
    sys.exit(1)

# 测试5: 检查配置文件
print("\n【测试5】 检查配置...")
try:
    config_manager = ConfigManager()
    tts_config = config_manager.get_tts_config()
    print(f"✓ 配置加载成功")
    print(f"  默认引擎: {tts_config.get('default_engine')}")
    print(f"  默认音色: {tts_config.get('edge', {}).get('default_voice')}")
except Exception as e:
    print(f"✗ 配置加载失败: {e}")
    sys.exit(1)

# 所有测试通过
print("\n" + "=" * 60)
print("  ✅ 所有测试通过!")
print("=" * 60)
print("\n下一步:")
print("  1. 运行示例: python cli.py convert test_novel.txt --voice xiaoxiao")
print("  2. 查看文档: QUICK_START.md")
print("  3. 列出音色: python cli.py voices")
print("\n祝使用愉快! 🎉")
