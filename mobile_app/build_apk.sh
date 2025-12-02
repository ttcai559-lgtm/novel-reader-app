#!/bin/bash
# Android APK 自动构建脚本

echo "========================================"
echo "  TXT小说转有声读物 - APK构建"
echo "========================================"

# 检查环境
echo ""
echo "[1/5] 检查环境..."
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer未安装"
    echo "请运行: pip3 install buildozer cython"
    exit 1
fi
echo "✓ Buildozer已安装"

# 复制核心代码
echo ""
echo "[2/5] 复制核心代码..."
cp -r ../modules . 2>/dev/null || echo "modules已存在"
cp -r ../core . 2>/dev/null || echo "core已存在"
cp -r ../config . 2>/dev/null || echo "config已存在"
cp ../novel_to_audio.py . 2>/dev/null || echo "novel_to_audio.py已存在"
echo "✓ 核心代码准备完成"

# 清理旧构建
echo ""
echo "[3/5] 清理旧构建..."
buildozer android clean
echo "✓ 清理完成"

# 构建APK
echo ""
echo "[4/5] 开始构建APK（这可能需要20-30分钟）..."
buildozer -v android debug

# 检查结果
echo ""
echo "[5/5] 检查构建结果..."
if [ -f "bin/"*.apk ]; then
    echo "✅ APK构建成功！"
    echo ""
    echo "APK文件位置:"
    ls -lh bin/*.apk
    echo ""
    echo "安装到设备:"
    echo "  adb install bin/*.apk"
else
    echo "❌ APK构建失败"
    echo "请查看上方错误信息"
    exit 1
fi

echo ""
echo "========================================"
echo "  构建完成！"
echo "========================================"
