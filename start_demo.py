"""
快速演示脚本 - 直接测试TTS功能
"""
import sys
import asyncio
from pathlib import Path

print("=" * 60)
print("  APP_Tool - TXT小说转有声读物 演示")
print("=" * 60)

# 步骤1: 测试导入
print("\n[1/4] 检查依赖...")
try:
    import edge_tts
    print("  OK: edge-tts")
except ImportError:
    print("  ERROR: 请先安装: pip install edge-tts")
    sys.exit(1)

try:
    from loguru import logger
    print("  OK: loguru")
except ImportError:
    print("  ERROR: 请先安装: pip install loguru")
    sys.exit(1)

try:
    import chardet
    print("  OK: chardet")
except ImportError:
    print("  ERROR: 请先安装: pip install chardet")
    sys.exit(1)

# 步骤2: 测试TTS
print("\n[2/4] 测试TTS合成...")

async def test_tts():
    # 创建输出目录
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 测试文本
    text = "你好，这是APP_Tool的测试。欢迎使用小说转有声读物功能。"
    output_file = "data/output/demo_test.mp3"

    print(f"  合成文本: {text}")
    print(f"  输出文件: {output_file}")

    # 使用Edge TTS
    voice = "zh-CN-XiaoxiaoNeural"  # 晓晓音色
    communicate = edge_tts.Communicate(text, voice)

    await communicate.save(output_file)

    if Path(output_file).exists():
        print(f"  SUCCESS: 音频已生成!")
        print(f"  文件大小: {Path(output_file).stat().st_size / 1024:.1f} KB")
        return True
    return False

# 运行测试
try:
    if asyncio.run(test_tts()):
        print("\n[3/4] 列出可用音色...")

        async def list_voices():
            voices = await edge_tts.list_voices()
            chinese_voices = [v for v in voices if v['Locale'].startswith('zh-CN')]

            print(f"\n  找到 {len(chinese_voices)} 个中文音色:")
            print("  " + "-" * 56)
            for i, v in enumerate(chinese_voices[:8], 1):
                gender_emoji = "女" if v['Gender'] == 'Female' else "男"
                print(f"  {i}. [{gender_emoji}] {v['ShortName']}")
            print("  " + "-" * 56)

        asyncio.run(list_voices())

        print("\n[4/4] 测试完成!")
        print("=" * 60)
        print("\n下一步，你可以:")
        print("  1. 播放生成的音频: data/output/demo_test.mp3")
        print("  2. 转换测试小说: python cli.py convert test_novel.txt")
        print("  3. 查看使用说明: QUICK_START.md")
        print("\n提示: 如果要合并音频，需要先安装FFmpeg")
        print("      查看安装指南: install_ffmpeg.md")
        print("=" * 60)
    else:
        print("\nERROR: TTS测试失败，请检查网络连接")

except Exception as e:
    print(f"\nERROR: {e}")
    print("\n可能的原因:")
    print("  1. 网络问题（Edge TTS需要联网）")
    print("  2. 依赖未正确安装")
    print("\n请先运行: pip install edge-tts loguru chardet PyYAML")
