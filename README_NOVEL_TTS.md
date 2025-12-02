# APP_Tool - TXT小说转有声读物工具 📚🎧

> **将任何TXT小说转换为高质量AI配音的有声读物**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ 功能特点

### 核心功能
- ✅ **TXT转MP3**: 一键将小说转换为有声读物
- 🎙️ **多种音色**: 8+种优质中文AI音色（男声/女声/特色音）
- 🎵 **高音质输出**: 支持多种音频格式和质量设置
- 📖 **智能章节识别**: 自动检测并分割章节
- ⚡ **并发处理**: 多线程加速合成
- 🔄 **自动编码检测**: 支持UTF-8、GBK等多种编码

### 音频功能
- 🎚️ **倍速播放**: 0.5x - 2.0x速度调节
- 🔊 **音量控制**: 自由调整音量
- 🎼 **音频合并**: 将多章节合并为单个文件
- 🎛️ **音质优化**: 音量标准化、动态压缩
- 📱 **格式转换**: MP3/WAV/M4A/OGG多格式支持

### 易用性
- 💻 **命令行工具**: 简单直观的CLI界面
- 🐍 **Python API**: 灵活的编程接口
- ⚙️ **配置管理**: YAML配置文件
- 📊 **进度显示**: 实时显示转换进度
- 🔍 **详细日志**: 完整的操作日志

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆或下载项目
cd D:\Python_file\APP_Tool

# 安装Python依赖
pip install -r requirements.txt

# 安装FFmpeg（音频处理必需）
# Windows: 下载 https://ffmpeg.org 并添加到PATH
# Linux: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg
```

### 2. 基础使用

```bash
# 转换小说（最简单）
python cli.py convert "小说.txt"

# 使用指定音色
python cli.py convert "小说.txt" --voice xiaoxiao

# 转换并合并所有章节
python cli.py convert "小说.txt" --merge

# 查看所有可用音色
python cli.py voices
```

### 3. 快速测试

```bash
# 使用项目自带的测试小说
python cli.py convert test_novel.txt --voice xiaoxiao

# 测试单句合成
python cli.py test "你好，欢迎使用APP_Tool" test.mp3 -v xiaoxiao

# 播放生成的音频
python cli.py play test.mp3
```

---

## 📖 详细文档

- **快速开始**: [QUICK_START.md](QUICK_START.md) - 5分钟上手指南
- **项目设计**: [PROJECT_DESIGN.md](PROJECT_DESIGN.md) - 完整架构设计
- **API文档**: 查看各模块代码中的文档字符串

---

## 🎨 音色展示

### 推荐音色列表

| 简称 | 完整ID | 描述 | 推荐场景 |
|-----|--------|------|---------|
| **xiaoxiao** ⭐ | zh-CN-XiaoxiaoNeural | 温柔女声 | 现代言情、都市 |
| **xiaoyi** | zh-CN-XiaoyiNeural | 甜美女声 | 轻小说、校园 |
| **xiaomeng** | zh-CN-XiaomengNeural | 少女音 | 少女向小说 |
| **xiaoyan** | zh-CN-XiaoyanNeural | 成熟女声 | 职场、悬疑 |
| **yunxi** ⭐ | zh-CN-YunxiNeural | 青年男声 | 都市、玄幻 |
| **yunyang** | zh-CN-YunyangNeural | 磁性男声 | 武侠、仙侠 |
| **yunjian** | zh-CN-YunjianNeural | 沉稳男声 | 历史、军事 |
| **yunxia** | zh-CN-YunxiaNeural | 播音腔 | 纪实类 |

⭐ = 最受欢迎

---

## 💻 使用示例

### 命令行方式

```bash
# 示例1: 转换网络小说
python cli.py convert "斗破苍穹.txt" --voice yunxi --merge

# 示例2: 批量转换（Windows批处理）
for %f in (*.txt) do python cli.py convert "%f" --voice xiaoxiao

# 示例3: 播放音频（1.5倍速）
python cli.py play "output/chapter1.mp3" --speed 1.5

# 示例4: 合并章节音频
python cli.py merge ch1.mp3 ch2.mp3 ch3.mp3 full.mp3
```

### Python脚本方式

```python
from novel_to_audio import NovelToAudio

# 初始化
converter = NovelToAudio()

# 转换小说
result = converter.convert(
    novel_path="小说.txt",
    merge=True,
    voice="xiaoxiao"
)

# 查看结果
print(f"成功: {result['tasks_completed']}/{result['tasks_total']}")
print(f"输出: {result['output_dir']}")

# 播放音频
if result['merged_file']:
    converter.play_audio(result['merged_file'], speed=1.2)
```

---

## 📂 项目结构

```
APP_Tool/
├── modules/               # 功能模块
│   ├── novel_reader/     # 文本处理
│   ├── tts_engine/       # TTS引擎
│   └── audio_processor/  # 音频处理
├── core/                 # 核心功能
│   ├── config_manager.py # 配置管理
│   └── task_manager.py   # 任务管理
├── config/               # 配置文件
│   └── default_config.yaml
├── data/                 # 数据目录
│   ├── output/          # 输出文件
│   └── cache/           # 缓存
├── cli.py               # 命令行工具
├── novel_to_audio.py    # 主程序
├── requirements.txt     # 依赖
└── README_NOVEL_TTS.md  # 本文档
```

---

## ⚙️ 配置

### 修改默认配置

创建 `config/user_config.yaml`:

```yaml
# TTS设置
tts:
  edge:
    default_voice: "zh-CN-XiaoxiaoNeural"
    speech_rate: 1.2  # 加快20%

# 音频质量
audio:
  output_format: "mp3"
  quality:
    bitrate: "256k"  # 高品质

# 性能优化
performance:
  max_workers: 8  # 并发数
```

### 查看当前配置

```bash
python cli.py config-show
```

---

## 🎯 完整工作流

### 场景: 转换一本100万字的网络小说

```bash
# 步骤1: 准备文件
# 确保小说文件为TXT格式，章节标题规范（如"第一章 XXX"）

# 步骤2: 测试转换
python cli.py test "测试文本,这是第一章的开头" test.mp3 -v xiaoxiao

# 步骤3: 转换完整小说
python cli.py convert "小说.txt" --voice xiaoxiao -o ./audiobooks

# 步骤4: 检查结果
# 输出目录: audiobooks/小说/
# 包含所有章节的MP3文件

# 步骤5: 如果满意，重新转换并合并
python cli.py convert "小说.txt" --voice xiaoxiao --merge -o ./audiobooks

# 步骤6: 播放完整有声书
python cli.py play "audiobooks/小说/小说_完整版.mp3" --speed 1.5
```

---

## 🔧 高级功能

### 1. 自定义章节识别

```yaml
# config/user_config.yaml
text:
  chapter_pattern: "^第[0-9]+章.*$"
```

### 2. 音频倍速导出

```python
from modules.audio_processor import AudioPlayerAdvanced

player = AudioPlayerAdvanced()
player.load('input.mp3')
player.export_with_speed('output_1.5x.mp3', speed=1.5)
```

### 3. 批量处理脚本

```python
import os
from novel_to_audio import NovelToAudio

converter = NovelToAudio()

for file in os.listdir('./novels'):
    if file.endswith('.txt'):
        print(f"处理: {file}")
        converter.convert(
            novel_path=f'./novels/{file}',
            voice='xiaoxiao',
            merge=True
        )
```

---

## 📊 性能参考

| 小说规模 | 字数 | 章节 | 转换时间* | 输出大小 |
|---------|------|------|----------|---------|
| 短篇 | 5万 | 20章 | ~2分钟 | ~100MB |
| 中篇 | 50万 | 200章 | ~20分钟 | ~1GB |
| 长篇 | 200万 | 800章 | ~80分钟 | ~4GB |
| 超长 | 500万+ | 2000章+ | ~3小时 | ~10GB+ |

\* 测试环境: i5-12400F, 16GB RAM, 并发数4, 网络良好

**优化建议**:
- 增加并发数可提升速度（根据CPU核心数）
- 使用SSD存储输出文件
- 确保网络稳定（Edge TTS需要联网）

---

## 🐛 常见问题

### Q1: 提示 "FFmpeg not found"
**A**: 需要安装FFmpeg并添加到系统PATH
```bash
# Windows: 下载 https://ffmpeg.org 并添加到环境变量
# 验证: ffmpeg -version
```

### Q2: 小说文件乱码
**A**: 程序会自动检测编码,如果还有问题:
```python
# 手动指定编码
converter.config.set('text.encoding', 'gbk')
```

### Q3: 章节识别不准确
**A**: 在配置文件中自定义章节正则表达式
```yaml
text:
  chapter_pattern: "^第[0-9]+章.*$"
```

### Q4: 转换速度慢
**A**: 调整并发数
```yaml
performance:
  max_workers: 8  # 根据CPU核心数调整
```

### Q5: 想要更多音色
**A**: 可以扩展支持其他TTS引擎（百度、阿里云、腾讯云）

---

## 🚧 未来功能

### 计划中的功能

- [ ] **多角色配音**: 自动识别对话,不同角色用不同音色
- [ ] **情感表达**: AI识别文本情感,调整语气
- [ ] **背景音乐**: 自动添加场景BGM
- [ ] **M4B格式**: 支持章节书签的有声书格式
- [ ] **GUI界面**: 图形化用户界面
- [ ] **移动端APP**: Android/iOS应用
- [ ] **云端处理**: 支持云端TTS和存储
- [ ] **实时预览**: 边转换边试听

---

## 📄 许可证

MIT License - 自由使用、修改和分发

---

## 🤝 贡献

欢迎提交Issue和Pull Request!

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📞 联系方式

- 项目地址: [GitHub](https://github.com/your-repo)
- 问题反馈: [Issues](https://github.com/your-repo/issues)

---

## 🙏 致谢

- **Microsoft Edge TTS**: 提供高质量免费TTS服务
- **pydub**: 强大的音频处理库
- **loguru**: 优雅的日志库
- **click**: 简洁的CLI框架

---

## ⭐ Star History

如果这个项目对你有帮助,请给一个Star支持一下! ⭐

---

**Happy Reading! 祝你听书愉快! 📚🎧**
