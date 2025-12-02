@echo off
chcp 65001 > nul
cls
echo ============================================================
echo   TXT小说转有声读物 - 立即测试
echo ============================================================
echo.

echo [1/3] 检查并安装依赖...
echo.

python -c "import edge_tts" 2>nul
if errorlevel 1 (
    echo 正在安装 edge-tts...
    pip install edge-tts --quiet
    if errorlevel 1 (
        echo.
        echo ERROR: 安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo OK: edge-tts 已安装
) else (
    echo OK: edge-tts 已安装
)

echo.
echo [2/3] 测试TTS合成...
echo.
echo 正在合成测试音频，请稍候...
echo.

python -c "import asyncio; import edge_tts; from pathlib import Path; Path('data/output').mkdir(parents=True, exist_ok=True); asyncio.run(edge_tts.Communicate('你好，欢迎使用小说转有声读物工具。这是一个测试。', 'zh-CN-XiaoxiaoNeural').save('data/output/test_demo.mp3')); print('SUCCESS: 音频生成成功！')"

if errorlevel 1 (
    echo.
    echo ERROR: 合成失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo [3/3] 测试完成！
echo ============================================================
echo.
echo SUCCESS: 音频已生成！
echo.
echo 文件位置: data\output\test_demo.mp3
echo.
echo 你可以:
echo   1. 打开 data\output\ 文件夹播放音频
echo   2. 转换完整小说: python cli.py convert test_novel.txt
echo   3. 查看使用说明: QUICK_START.md
echo.
echo ============================================================
echo.

echo 是否现在打开输出文件夹？(Y/N)
set /p choice=请选择:

if /i "%choice%"=="Y" (
    start "" "%CD%\data\output"
)

echo.
echo 按任意键退出...
pause > nul
