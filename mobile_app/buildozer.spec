[app]

# 应用信息
title = 小说转有声读物
package.name = novelreader
package.domain = com.apptool

# 源代码目录
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# 版本
version = 1.0.0

# Python依赖
requirements = python3,kivy,edge-tts,aiohttp,certifi,loguru,pyyaml,chardet,asyncio

# 主程序入口
entrypoint = main.py

# 图标和启动画面（可选）
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/presplash.png

# Android权限
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,WAKE_LOCK

# Android API级别
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31
android.accept_sdk_license = True

# Android架构
android.archs = arm64-v8a,armeabi-v7a

# 屏幕方向
orientation = portrait

# 全屏模式
fullscreen = 0

[buildozer]

# 日志级别
log_level = 2

# 警告为错误
warn_on_root = 1
