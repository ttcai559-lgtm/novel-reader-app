#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最简单的测试 - 直接合成一句话
"""
import asyncio
from pathlib import Path

async def main():
    print("测试开始...")

    # 导入edge-tts
    import edge_tts

    # 创建输出目录
    Path("data/output").mkdir(parents=True, exist_ok=True)

    # 合成音频
    text = "你好，欢迎使用APP_Tool小说转有声读物工具。"
    output = "data/output/simple_test.mp3"

    print(f"正在合成: {text}")
    print(f"输出文件: {output}")

    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output)

    if Path(output).exists():
        size = Path(output).stat().st_size / 1024
        print(f"\n成功! 文件大小: {size:.1f} KB")
        print(f"请播放文件: {output}")
        return True
    else:
        print("\n失败!")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        if result:
            print("\n提示: 你可以用任何音频播放器播放生成的MP3文件")
    except Exception as e:
        print(f"\n错误: {e}")
        print("请检查:")
        print("  1. edge-tts是否已安装: pip install edge-tts")
        print("  2. 网络连接是否正常")
