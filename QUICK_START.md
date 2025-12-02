# APP_Tool 快速开始指南

## 🚀 快速安装

### 1. 安装依赖

```bash
# 进入项目目录
cd D:\Python_file\APP_Tool

# 激活虚拟环境（如果有）
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装FFmpeg（必需，用于音频处理）

#### Windows:
1. 下载: https://ffmpeg.org/download.html
2. 解压并添加到系统PATH
3. 验证: `ffmpeg -version`

#### Linux:
```bash
sudo apt-get install ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
```

---

## 📖 基础使用

### 方式1: 使用命令行工具（推荐）

#### 1. 转换小说

```bash
# 基础转换
python cli.py convert "小说.txt"

# 使用指定音色
python cli.py convert "小说.txt" --voice xiaoxiao

# 转换并合并所有章节为单个MP3
python cli.py convert "小说.txt" --merge

# 指定输出目录
python cli.py convert "小说.txt" -o ./output
```

#### 2. 查看可用音色

```bash
python cli.py voices
```

**推荐音色:**
- `xiaoxiao` - 晓晓（温柔女声）⭐
- `xiaoyi` - 晓伊（甜美女声）
- `xiaomeng` - 晓梦（少女音）
- `yunxi` - 云希（青年男声）⭐
- `yunyang` - 云扬（磁性男声）
- `yunjian` - 云健（沉稳男声）

#### 3. 播放音频

```bash
# 普通播放
python cli.py play "output/chapter1.mp3"

# 1.5倍速播放
python cli.py play "output/chapter1.mp3" --speed 1.5

# 调整音量
python cli.py play "output/chapter1.mp3" --volume 0.5
```

#### 4. 快速测试

```bash
# 测试单句合成
python cli.py test "你好，这是一个测试。" test.mp3 -v xiaoxiao
```

#### 5. 合并音频文件

```bash
# 合并多个章节
python cli.py merge ch1.mp3 ch2.mp3 ch3.mp3 full.mp3

# 设置章节间静音1秒
python cli.py merge *.mp3 full.mp3 --silence 1000
```

---

### 方式2: 使用Python代码

```python
from novel_to_audio import NovelToAudio

# 初始化转换器
converter = NovelToAudio()

# 转换小说
result = converter.convert(
    novel_path="三体.txt",
    merge=True,           # 合并所有章节
    voice="xiaoxiao"      # 使用晓晓音色
)

print(f"转换完成！输出目录: {result['output_dir']}")
```

---

## 🎯 完整示例

### 示例1: 转换网络小说

假设你有一个TXT格式的小说 `凡人修仙传.txt`:

```bash
# 使用温柔女声，转换并合并
python cli.py convert "凡人修仙传.txt" --voice xiaoxiao --merge -o ./audiobooks

# 输出:
# audiobooks/
# ├── 凡人修仙传/
# │   ├── 001_00.mp3
# │   ├── 001_01.mp3
# │   ├── ...
# │   └── 凡人修仙传_完整版.mp3  ← 合并后的完整有声书
```

### 示例2: 批量转换

```python
from novel_to_audio import NovelToAudio

converter = NovelToAudio()

# 批量转换多部小说
novels = ["小说1.txt", "小说2.txt", "小说3.txt"]
voice_map = {
    "小说1.txt": "xiaoxiao",  # 女声
    "小说2.txt": "yunxi",     # 男声
    "小说3.txt": "xiaoyi"     # 甜美女声
}

for novel in novels:
    print(f"\n处理: {novel}")
    result = converter.convert(
        novel_path=novel,
        voice=voice_map.get(novel, "xiaoxiao"),
        merge=True
    )
    print(f"完成: {result['merged_file']}")
```

### 示例3: 只转换特定章节

```python
from modules.novel_reader import TextProcessor

processor = TextProcessor()

# 加载小说
novel = processor.load_novel("小说.txt")

# 只转换第10-20章
chapters_to_convert = novel['chapters'][9:20]  # Python索引从0开始

# 转换这些章节
converter = NovelToAudio()
for chapter in chapters_to_convert:
    output_path = f"output/{chapter.index}_{chapter.title}.mp3"
    converter.convert_chapter(
        chapter_text=chapter.content,
        chapter_title=chapter.title,
        output_path=output_path,
        voice="xiaoxiao"
    )
```

---

## ⚙️ 配置文件

### 查看当前配置

```bash
python cli.py config-show
```

### 修改配置

编辑文件: `config/user_config.yaml` (不存在则创建)

```yaml
# 示例：修改默认音色和语速
tts:
  edge:
    default_voice: "zh-CN-XiaoxiaoNeural"
    speech_rate: 1.2  # 加快20%

# 修改输出格式
audio:
  output_format: "mp3"
  quality:
    bitrate: "256k"  # 高品质
```

---

## 🎨 音色对比

| 音色简称 | 完整ID | 描述 | 适合内容 |
|---------|--------|------|----------|
| **xiaoxiao** | zh-CN-XiaoxiaoNeural | 温柔女声 | 现代言情、都市小说 |
| **xiaoyi** | zh-CN-XiaoyiNeural | 甜美女声 | 轻小说、青春校园 |
| **xiaomeng** | zh-CN-XiaomengNeural | 少女音 | 少女向、萌系小说 |
| **xiaoyan** | zh-CN-XiaoyanNeural | 成熟女声 | 职场、悬疑 |
| **yunxi** | zh-CN-YunxiNeural | 青年男声 | 现代都市、玄幻 |
| **yunyang** | zh-CN-YunyangNeural | 磁性男声 | 武侠、仙侠 |
| **yunjian** | zh-CN-YunjianNeural | 沉稳男声 | 历史、军事 |
| **yunxia** | zh-CN-YunxiaNeural | 播音腔 | 纪实、新闻式 |

---

## 🔧 常见问题

### 1. FFmpeg not found

**问题**: 提示找不到FFmpeg

**解决**:
```bash
# 安装FFmpeg
# Windows: 下载并添加到PATH
# Linux: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg

# 验证安装
ffmpeg -version
```

### 2. 编码问题

**问题**: 小说文件乱码

**解决**: 程序会自动检测编码，如果还有问题：
```python
# 手动指定编码
converter = NovelToAudio()
# 修改配置
converter.config.set('text.encoding', 'gbk')  # 或 'utf-8'
```

### 3. 章节识别错误

**问题**: 章节分割不准确

**解决**: 自定义章节模式
```yaml
# config/user_config.yaml
text:
  chapter_pattern: "^第[0-9]+章.*$"  # 正则表达式
```

### 4. 合成速度慢

**解决**: 增加并发数
```yaml
# config/user_config.yaml
performance:
  max_workers: 8  # 根据CPU核心数调整
```

### 5. 音频倍速播放

**问题**: 想要倍速播放

**解决**:
```bash
# 使用播放器倍速
python cli.py play audio.mp3 --speed 1.5

# 或者导出倍速音频
python -c "
from modules.audio_processor import AudioPlayerAdvanced
player = AudioPlayerAdvanced()
player.load('input.mp3')
player.export_with_speed('output_1.5x.mp3', speed=1.5)
"
```

---

## 📊 性能参考

**测试环境**: Windows 11, i5-12400F, 16GB RAM

| 小说字数 | 章节数 | 转换时间 | 输出大小 |
|---------|--------|---------|----------|
| 10万字 | 50章 | ~5分钟 | ~200MB |
| 50万字 | 200章 | ~20分钟 | ~1GB |
| 100万字 | 400章 | ~40分钟 | ~2GB |

**提示**:
- 使用并发可大幅提升速度
- Edge TTS需要网络连接
- 合并操作在章节较多时会较慢

---

## 🎯 进阶技巧

### 1. 自动添加背景音乐（未来功能）

```python
# 即将支持
converter.convert(
    novel_path="小说.txt",
    enable_bgm=True,
    bgm_volume=0.1
)
```

### 2. 多角色配音（规划中）

```python
# 即将支持
converter.convert(
    novel_path="小说.txt",
    multi_voice=True,
    narrator_voice="xiaoxiao",    # 旁白
    male_voice="yunxi",           # 男角色
    female_voice="xiaoyi"         # 女角色
)
```

### 3. 导出带章节的M4B格式（规划中）

```bash
# 即将支持
python cli.py convert "小说.txt" --format m4b --chapters
```

---

## 📝 完整命令参考

```bash
# 查看帮助
python cli.py --help
python cli.py convert --help

# 转换命令
python cli.py convert <小说路径> [选项]
  --output, -o      输出目录
  --voice, -v       音色选择
  --merge          合并章节
  --config, -c     配置文件

# 音色列表
python cli.py voices

# 播放音频
python cli.py play <音频路径> [选项]
  --speed, -s      播放速度 (0.5-2.0)
  --volume, -v     音量 (0.0-1.0)

# 快速测试
python cli.py test <文本> <输出路径> [选项]
  --voice, -v      音色
  --title, -t      标题

# 合并音频
python cli.py merge <文件1> <文件2> ... <输出>
  --silence, -s    静音间隔(毫秒)

# 查看配置
python cli.py config-show
```

---

## 💡 小贴士

1. **首次使用建议**: 先用小文件测试各种音色，找到最喜欢的
2. **推荐工作流**:
   - 先不合并，听几章确认质量
   - 满意后再重新转换并合并
3. **节省时间**: 使用缓存功能，相同文本不会重复合成
4. **音质提升**: 配置文件中设置更高的比特率
5. **批量处理**: 写Python脚本批量转换多本书

---

## 🆘 获取帮助

- 查看完整文档: `README.md`
- 项目设计: `PROJECT_DESIGN.md`
- 提交问题: GitHub Issues (如果有)

---

**祝你听书愉快！🎧📚**
