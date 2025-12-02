# APP_Tool 安装指南

## 📦 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **磁盘空间**: 至少 500MB 可用空间
- **网络**: 需要联网（Edge TTS需要）
- **内存**: 建议 4GB+

---

## 🚀 安装步骤

### 方法1: 标准安装（推荐）

#### 步骤1: 安装Python依赖

```bash
# 进入项目目录
cd D:\Python_file\APP_Tool

# 安装依赖包
pip install -r requirements.txt
```

#### 步骤2: 安装FFmpeg

**FFmpeg是音频处理必需的工具**

##### Windows:
1. 访问 https://ffmpeg.org/download.html#build-windows
2. 下载 "ffmpeg-release-essentials.zip"
3. 解压到 `C:\ffmpeg`
4. 添加到系统PATH:
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → 系统变量 → Path → 编辑
   - 新建 → 输入 `C:\ffmpeg\bin`
   - 确定保存

5. 验证安装:
```bash
ffmpeg -version
```

##### macOS:
```bash
# 使用Homebrew安装
brew install ffmpeg

# 验证
ffmpeg -version
```

##### Linux (Ubuntu/Debian):
```bash
# 安装FFmpeg
sudo apt-get update
sudo apt-get install ffmpeg

# 验证
ffmpeg -version
```

#### 步骤3: 验证安装

```bash
# 运行快速测试
python quick_test.py
```

如果看到 "✅ 所有测试通过!"，说明安装成功！

---

### 方法2: 使用虚拟环境（推荐专业用户）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装FFmpeg (同上)

# 运行测试
python quick_test.py
```

---

## 🔍 依赖说明

### 核心依赖

| 包名 | 版本 | 用途 |
|-----|------|-----|
| edge-tts | 6.1.12 | 微软Edge TTS引擎 |
| pydub | 0.25.1 | 音频处理 |
| pygame | 2.5.2 | 音频播放 |
| chardet | 5.2.0 | 编码检测 |
| loguru | 0.7.2 | 日志系统 |
| PyYAML | 6.0.1 | 配置文件 |
| click | 8.1.7 | 命令行工具 |
| tqdm | 4.66.1 | 进度条 |

### 可选依赖

```bash
# 如果需要使用云端TTS
pip install baidu-aip  # 百度AI
pip install alibabacloud-nls20180518  # 阿里云
pip install tencentcloud-sdk-python  # 腾讯云
```

---

## 🐛 常见安装问题

### Q1: pip install 很慢

**解决**: 使用国内镜像源

```bash
# 临时使用
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久设置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 安装pydub失败

**原因**: pydub依赖FFmpeg

**解决**:
1. 先安装FFmpeg（见上方步骤2）
2. 再安装pydub: `pip install pydub`

### Q3: pygame安装失败 (Windows)

**解决**:
```bash
# 下载对应Python版本的wheel文件
# 访问: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
# 安装: pip install pygame-2.5.2-cp39-cp39-win_amd64.whl
```

### Q4: ImportError: No module named 'modules'

**原因**: 没有在正确的目录下运行

**解决**:
```bash
# 确保在项目根目录
cd D:\Python_file\APP_Tool
python cli.py --help
```

### Q5: edge-tts 网络错误

**原因**: 网络问题或需要代理

**解决**:
```bash
# 测试网络
ping speech.platform.bing.com

# 如果需要代理
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
```

---

## ✅ 验证安装

### 完整测试流程

```bash
# 1. 运行自动测试
python quick_test.py

# 2. 列出音色
python cli.py voices

# 3. 测试单句合成
python cli.py test "你好,世界" test.mp3

# 4. 转换测试小说
python cli.py convert test_novel.txt --voice xiaoxiao

# 5. 播放生成的音频
python cli.py play data/output/test_novel/001_00.mp3
```

如果以上命令都能正常运行，恭喜你安装成功！🎉

---

## 📋 安装检查清单

- [ ] Python 3.8+ 已安装
- [ ] pip 可以正常使用
- [ ] FFmpeg 已安装并加入PATH
- [ ] 所有Python依赖已安装
- [ ] `python quick_test.py` 通过
- [ ] `python cli.py voices` 能列出音色
- [ ] 能成功合成测试音频

---

## 🔄 更新

```bash
# 更新所有依赖到最新版本
pip install -r requirements.txt --upgrade

# 更新特定包
pip install edge-tts --upgrade
```

---

## 🗑️ 卸载

```bash
# 卸载依赖
pip uninstall -r requirements.txt -y

# 删除项目文件
# Windows: rmdir /s D:\Python_file\APP_Tool
# Linux/Mac: rm -rf /path/to/APP_Tool
```

---

## 📞 获取帮助

如果遇到其他安装问题:

1. 查看 [QUICK_START.md](QUICK_START.md)
2. 查看 [常见问题](README_NOVEL_TTS.md#常见问题)
3. 提交 Issue (如果是GitHub项目)

---

## 🎯 下一步

安装完成后,请查看:

- **快速开始**: [QUICK_START.md](QUICK_START.md)
- **完整文档**: [README_NOVEL_TTS.md](README_NOVEL_TTS.md)
- **项目设计**: [PROJECT_DESIGN.md](PROJECT_DESIGN.md)

**祝使用愉快！🚀**
