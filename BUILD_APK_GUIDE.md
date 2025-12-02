# 📱 Android APK 打包完整指南

## 🎯 概述

将TXT小说转有声读物工具打包成Android APK，可以在手机上直接安装使用。

---

## 📋 环境要求

### 系统要求
- **操作系统**: Linux (Ubuntu 20.04+推荐) 或 macOS
- **Python**: 3.8-3.10
- **磁盘空间**: 至少10GB
- **内存**: 8GB+推荐

⚠️ **注意**: Windows不支持直接打包，需要使用WSL2或虚拟机

---

## 🚀 方法1: 使用Buildozer（推荐）

### 步骤1: 安装Buildozer

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3-pip build-essential git python3-dev \
    ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev \
    libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    openjdk-11-jdk unzip

# 安装Cython和Buildozer
pip3 install --upgrade cython buildozer

# macOS
brew install python@3.9
brew install ffmpeg sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip3 install --upgrade cython buildozer
```

### 步骤2: 准备项目

```bash
cd D:\Python_file\APP_Tool\mobile_app

# 复制核心模块到mobile_app目录
cp -r ../modules .
cp -r ../core .
cp -r ../config .
cp ../novel_to_audio.py .
```

### 步骤3: 初始化Buildozer

```bash
buildozer init
# 会生成 buildozer.spec 文件（已创建）
```

### 步骤4: 构建APK

```bash
# Debug版本（用于测试）
buildozer -v android debug

# Release版本（用于发布）
buildozer -v android release
```

### 步骤5: 获取APK

```bash
# APK位置
ls bin/

# 输出:
# novelreader-1.0.0-debug.apk  (Debug版)
# novelreader-1.0.0-release-unsigned.apk  (Release版)
```

---

## 🔧 方法2: 使用GitHub Actions（自动化）

### 创建GitHub Actions工作流

```yaml
# .github/workflows/build-apk.yml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y python3-pip build-essential git
        pip install buildozer cython

    - name: Build APK
      working-directory: ./mobile_app
      run: |
        buildozer android debug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: novelreader-apk
        path: mobile_app/bin/*.apk
```

---

## 🌐 方法3: 使用在线服务

### Replit + Buildozer

1. 访问 https://replit.com
2. 创建Python项目
3. 上传代码
4. 安装Buildozer
5. 运行构建命令

### Google Colab

```python
# 在Colab中运行
!apt-get install -y python3-pip build-essential git
!pip install buildozer cython

# 克隆项目
!git clone <your-repo>
%cd mobile_app

# 构建
!buildozer android debug
```

---

## 📦 打包配置说明

### buildozer.spec 关键配置

```ini
[app]
# 应用名称
title = 小说转有声读物

# 包名（反向域名）
package.name = novelreader
package.domain = com.apptool

# 版本号
version = 1.0.0

# Python依赖
requirements = python3,kivy,edge-tts,aiohttp,loguru,pyyaml,chardet

# Android权限
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 最低Android版本
android.minapi = 21  # Android 5.0
android.api = 31     # Android 12

# 架构
android.archs = arm64-v8a,armeabi-v7a
```

---

## 🎨 添加图标和启动画面

### 1. 准备图片

- **图标**: `assets/icon.png` (512x512px, PNG)
- **启动画面**: `assets/presplash.png` (1280x720px, PNG)

### 2. 修改buildozer.spec

```ini
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png
```

---

## 🔐 签名APK（Release版本）

### 生成密钥库

```bash
keytool -genkey -v -keystore my-release-key.keystore \
    -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# 输入密钥库密码和信息
```

### 签名APK

```bash
# 使用jarsigner签名
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
    -keystore my-release-key.keystore \
    bin/novelreader-1.0.0-release-unsigned.apk my-key-alias

# 对齐APK
zipalign -v 4 \
    bin/novelreader-1.0.0-release-unsigned.apk \
    bin/novelreader-1.0.0-release.apk
```

---

## 🧪 测试APK

### 方法1: 安装到真机

```bash
# 启用USB调试
# 连接手机到电脑

# 安装APK
adb install bin/novelreader-1.0.0-debug.apk

# 查看日志
adb logcat | grep python
```

### 方法2: 使用模拟器

```bash
# 安装Android Studio
# 创建虚拟设备
# 拖拽APK到模拟器安装
```

---

## 📊 APK规格

### 预期结果

- **文件大小**: 约40-60MB
- **支持系统**: Android 5.0+
- **架构**: ARM64, ARM32
- **权限**:
  - 互联网访问（TTS需要）
  - 读写存储（导入TXT，保存音频）
  - 保持唤醒（转换时）

---

## ⚠️ 常见问题

### Q1: Buildozer构建失败

**A**: 检查依赖是否完整安装

```bash
buildozer android clean
buildozer -v android debug
```

### Q2: Windows下无法打包

**A**: 使用WSL2

```bash
# 安装WSL2
wsl --install

# 进入WSL
wsl

# 按Linux步骤操作
```

### Q3: APK安装后闪退

**A**: 检查日志

```bash
adb logcat | grep python
```

### Q4: 缺少某个Python包

**A**: 修改buildozer.spec中的requirements

```ini
requirements = python3,kivy,edge-tts,aiohttp,新包名
```

---

## 🎯 快速打包流程（总结）

```bash
# 1. 准备环境（Ubuntu）
sudo apt install -y build-essential python3-dev
pip3 install buildozer cython

# 2. 进入项目
cd D:\Python_file\APP_Tool\mobile_app

# 3. 复制核心代码
cp -r ../modules ../core ../config ../novel_to_audio.py .

# 4. 构建APK
buildozer -v android debug

# 5. 获取APK
# 文件: bin/novelreader-1.0.0-debug.apk

# 6. 安装测试
adb install bin/novelreader-1.0.0-debug.apk
```

---

## 🌟 优化建议

### 1. 减小APK大小

```ini
# buildozer.spec
android.archs = arm64-v8a  # 只打包64位
```

### 2. 加快构建速度

```bash
# 使用缓存
buildozer android debug --cache
```

### 3. 多线程构建

```bash
# 使用多核CPU
export MAKEFLAGS="-j$(nproc)"
buildozer android debug
```

---

## 📞 需要帮助？

### 在线资源

- Buildozer文档: https://buildozer.readthedocs.io/
- Kivy文档: https://kivy.org/doc/stable/
- Android开发者: https://developer.android.com/

### 社区支持

- Kivy Discord: https://chat.kivy.org/
- Stack Overflow: #kivy #buildozer

---

## 🎊 完成！

按照以上步骤，你将得到:

✅ **novelreader-1.0.0-debug.apk** - 可安装的Android应用
✅ 支持导入TXT小说
✅ 支持多种AI音色
✅ 支持倍速播放
✅ 内置音频播放器

**立即在手机上享受有声小说吧！📱📚🎧**
