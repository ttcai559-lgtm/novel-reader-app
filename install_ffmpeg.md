# FFmpeg 安装指南（Windows）

## 方法1: 自动下载安装（推荐）

### 使用 Chocolatey

```powershell
# 以管理员身份打开PowerShell
# 安装 Chocolatey（如果没有）
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装 FFmpeg
choco install ffmpeg
```

## 方法2: 手动下载安装

### 步骤1: 下载FFmpeg

访问: https://www.gyan.dev/ffmpeg/builds/

下载: **ffmpeg-release-essentials.zip**

### 步骤2: 解压

解压到: `C:\ffmpeg`

### 步骤3: 添加到PATH

1. 右键 "此电脑" → 属性
2. 高级系统设置 → 环境变量
3. 系统变量 → 找到 "Path" → 编辑
4. 新建 → 输入 `C:\ffmpeg\bin`
5. 确定保存

### 步骤4: 验证

打开新的命令行窗口:

```bash
ffmpeg -version
```

如果显示版本信息，说明安装成功！

## 方法3: 使用winget（Windows 10+）

```powershell
winget install ffmpeg
```

---

## ⚠️ 临时方案：不安装FFmpeg

如果暂时不想安装FFmpeg，可以：

1. **只使用TTS合成功能**（不合并音频）
2. **播放功能使用pygame**（不需要FFmpeg）

运行:
```bash
python cli.py convert test_novel.txt --voice xiaoxiao
# 不使用 --merge 参数，避免音频合并
```

---

## 📞 需要帮助？

如果安装遇到问题，可以：
1. 使用方法3（最简单）
2. 或暂时跳过，先体验TTS合成功能
