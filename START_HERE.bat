@echo off
chcp 65001 > nul
echo ============================================================
echo   APP_Tool - TXT小说转有声读物工具
echo ============================================================
echo.

echo [步骤1] 激活虚拟环境...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo OK: 虚拟环境已激活
) else if exist "..\tool_project\venv\Scripts\activate.bat" (
    call ..\tool_project\venv\Scripts\activate.bat
    echo OK: 虚拟环境已激活
) else (
    echo WARNING: 未找到虚拟环境，使用系统Python
)

echo.
echo [步骤2] 检查依赖...
python -c "import edge_tts; print('OK: edge-tts')" 2>nul
if errorlevel 1 (
    echo ERROR: edge-tts未安装
    echo 正在安装...
    pip install edge-tts loguru chardet PyYAML click tqdm
)

echo.
echo [步骤3] 运行演示...
python start_demo.py

echo.
echo ============================================================
echo 按任意键退出...
pause > nul
