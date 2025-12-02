#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本地TTS测试 - 不需要网络
使用Windows系统自带的语音引擎
"""
import pyttsx3
from pathlib import Path

def test_local_tts():
    print("测试本地TTS（Windows SAPI5）...")
    print("优点：完全离线，不需要网络")
    print("缺点：声音较机械\n")

    try:
        # 初始化引擎
        engine = pyttsx3.init()

        # 获取可用音色
        voices = engine.getProperty('voices')
        print(f"找到 {len(voices)} 个系统音色:")
        for i, voice in enumerate(voices):
            print(f"  {i+1}. {voice.name}")
        print()

        # 设置中文音色（如果有）
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                print(f"使用音色: {voice.name}\n")
                break

        # 设置参数
        engine.setProperty('rate', 150)  # 语速
        engine.setProperty('volume', 1.0)  # 音量

        # 测试文本
        text = "你好，这是本地TTS测试。我是Windows系统自带的语音引擎。"

        print("正在合成音频...")

        # 创建输出目录
        output_dir = Path("data/output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成音频
        output_file = output_dir / "local_test.mp3"
        engine.save_to_file(text, str(output_file))
        engine.runAndWait()

        if output_file.exists():
            size = output_file.stat().st_size / 1024
            print(f"\n✓ 成功!")
            print(f"文件: {output_file}")
            print(f"大小: {size:.1f} KB")
            print(f"\n你可以播放这个文件听听效果。")
            print(f"虽然是机械音，但完全离线可用！")
            return True
        else:
            print("\n✗ 生成失败")
            return False

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        print("\n可能需要安装: pip install pyttsx3")
        print("或者: pip install pywin32")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("  本地TTS测试（不需要网络）")
    print("=" * 60)
    print()

    result = test_local_tts()

    if result:
        print("\n" + "=" * 60)
        print("  测试成功！")
        print("=" * 60)
        print("\n虽然本地TTS音质不如Edge TTS，")
        print("但如果网络有问题，可以暂时使用。")
    else:
        print("\n" + "=" * 60)
        print("  测试失败")
        print("=" * 60)
