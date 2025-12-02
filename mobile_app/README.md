# 📱 TXT小说转有声读物 - Android APP

## 🎯 功能特性

- ✅ 导入TXT小说文件
- ✅ 8+种AI音色选择
- ✅ 智能章节识别
- ✅ 高质量TTS合成
- ✅ 内置音频播放器
- ✅ 倍速播放（0.5x-2.0x）
- ✅ 进度保存和跳转

---

## 📱 APP界面预览

### 主页面
- 文件选择器（浏览TXT文件）
- 音色选择（8种AI音色）
- 语速调节（0.5x-2.0x）
- 转换按钮
- 进度显示

### 播放器页面
- 封面显示
- 进度条
- 播放控制（播放/暂停/快进/快退）
- 倍速播放
- 时间显示

---

## 🚀 构建APK

### 环境要求

- **系统**: Linux (Ubuntu 20.04+) 或 macOS
- **Python**: 3.8-3.10
- **磁盘**: 10GB+
- **内存**: 8GB+

### 快速构建

```bash
# 1. 安装依赖
sudo apt-get install -y python3-pip build-essential git python3-dev
pip3 install buildozer cython

# 2. 构建APK
./build_apk.sh

# 或手动构建
buildozer -v android debug
```

### 获取APK

```bash
# APK位置
ls bin/

# 输出:
novelreader-1.0.0-debug.apk
```

---

## 📦 安装测试

### 安装到真机

```bash
# 连接手机（启用USB调试）
adb devices

# 安装APK
adb install bin/novelreader-1.0.0-debug.apk
```

### 使用模拟器

1. 安装Android Studio
2. 创建虚拟设备
3. 拖拽APK到模拟器

---

## 🎨 自定义

### 修改应用名称

编辑 `buildozer.spec`:
```ini
title = 你的应用名
```

### 添加图标

1. 准备512x512px的PNG图标
2. 放置到 `assets/icon.png`
3. 修改 `buildozer.spec`:
```ini
icon.filename = %(source.dir)s/assets/icon.png
```

### 修改包名

```ini
package.name = yourappname
package.domain = com.yourdomain
```

---

## 📊 技术栈

- **UI框架**: Kivy 2.3.0
- **TTS引擎**: Microsoft Edge TTS
- **音频播放**: Kivy Audio
- **打包工具**: Buildozer
- **目标平台**: Android 5.0+

---

## 🔧 故障排除

### 构建失败

```bash
# 清理并重试
buildozer android clean
buildozer -v android debug
```

### 安装后闪退

```bash
# 查看日志
adb logcat | grep python
```

### 缺少权限

修改 `buildozer.spec`:
```ini
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
```

---

## 📖 完整文档

详细打包指南请参考:
- [BUILD_APK_GUIDE.md](../BUILD_APK_GUIDE.md)

---

## 🎊 完成！

构建成功后，你将得到:
- ✅ 完整的Android APK
- ✅ 可在手机上直接安装使用
- ✅ 无需电脑，手机独立运行

**立即享受移动端有声小说吧！📱📚🎧**
