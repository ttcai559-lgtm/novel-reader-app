# APP工具包项目设计方案

## 项目概述

**项目名称**: APP_Tool - Python多功能APK工具包
**核心功能**: TXT小说转有声读物
**扩展能力**: 可持续添加更多实用工具模块

---

## 第一期功能：TXT小说转有声读物

### 功能特性

#### 1. 文本处理
- 支持导入TXT格式小说文件
- 自动识别文本编码（UTF-8, GBK, GB2312等）
- 智能章节识别和分割
- 文本预处理（去除特殊字符、标点优化）
- 支持长文本智能分段（避免单次合成过长）

#### 2. 多引擎TTS支持

##### 本地离线引擎
- **pyttsx3**: Windows SAPI5引擎
  - 优点：完全离线，免费
  - 缺点：声音较机械

- **edge-tts**: 微软Edge浏览器TTS
  - 优点：免费，音质优秀，多语言多音色
  - 缺点：需要网络连接

- **ChatTTS**: 开源对话式TTS
  - 优点：声音自然，支持情感
  - 缺点：需要本地模型

##### 云端AI引擎
- **百度AI语音合成**
  - 提供多种音色选择
  - 支持语速、音调、音量调节

- **阿里云TTS**
  - 高质量合成效果
  - 丰富的声音角色库

- **腾讯云TTS**
  - 自然度高
  - 支持SSML标记语言

- **OpenAI TTS** (可选)
  - 顶级AI语音效果
  - 多种自然声音

#### 3. 音色选择系统

```
音色库分类：
├── 男声
│   ├── 磁性男声
│   ├── 青年男声
│   ├── 沉稳男声
│   └── 播音腔男声
├── 女声
│   ├── 甜美女声
│   ├── 温柔女声
│   ├── 成熟女声
│   └── 少女音
└── 特色音
    ├── 儿童音
    ├── 方言音（可选）
    └── 情感音（AI生成）
```

#### 4. AI有声小说特效

##### 智能角色配音
- 自动识别对话内容
- 为不同角色分配不同音色
- 对话与旁白区分处理

##### 情感表达增强
- 识别句子情感（喜怒哀乐）
- 自动调整语气、语速
- 添加适当的停顿和重音

##### 背景音效（可选）
- 根据场景自动添加BGM
- 环境音效（雨声、风声等）
- 音效淡入淡出处理

#### 5. 音频处理功能
- 音频格式：MP3, WAV, M4A
- 音质选择：标准/高品质/无损
- 音量标准化处理
- 章节合并或独立导出
- 添加章节标记（M4B格式）

---

## 技术架构

### 核心模块设计

```
APP_Tool/
├── modules/                    # 功能模块
│   ├── novel_reader/          # 小说阅读器模块
│   │   ├── __init__.py
│   │   ├── text_processor.py  # 文本处理器
│   │   ├── chapter_parser.py  # 章节解析器
│   │   ├── encoding_detector.py # 编码检测
│   │   └── text_cleaner.py    # 文本清洗
│   │
│   ├── tts_engine/            # TTS引擎模块
│   │   ├── __init__.py
│   │   ├── base_tts.py        # TTS基类
│   │   ├── local_tts.py       # 本地引擎
│   │   │   ├── pyttsx3_engine.py
│   │   │   ├── edge_tts_engine.py
│   │   │   └── chattts_engine.py
│   │   └── cloud_tts.py       # 云端引擎
│   │       ├── baidu_tts.py
│   │       ├── aliyun_tts.py
│   │       ├── tencent_tts.py
│   │       └── openai_tts.py
│   │
│   ├── audio_processor/       # 音频处理模块
│   │   ├── __init__.py
│   │   ├── audio_merger.py    # 音频合并
│   │   ├── audio_normalizer.py # 音量标准化
│   │   ├── format_converter.py # 格式转换
│   │   └── metadata_editor.py  # 元数据编辑
│   │
│   ├── ai_enhancer/           # AI增强模块
│   │   ├── __init__.py
│   │   ├── emotion_detector.py # 情感检测
│   │   ├── role_detector.py    # 角色识别
│   │   ├── voice_selector.py   # 音色选择器
│   │   └── effect_processor.py # 特效处理
│   │
│   └── gui/                   # 图形界面模块
│       ├── __init__.py
│       ├── main_window.py     # 主窗口
│       ├── settings_dialog.py # 设置对话框
│       └── progress_dialog.py # 进度对话框
│
├── core/                      # 核心功能
│   ├── __init__.py
│   ├── config_manager.py      # 配置管理
│   ├── task_manager.py        # 任务管理
│   └── cache_manager.py       # 缓存管理
│
├── utils/                     # 工具类
│   ├── __init__.py
│   ├── logger.py              # 日志工具
│   ├── file_utils.py          # 文件工具
│   └── audio_utils.py         # 音频工具
│
├── config/                    # 配置文件
│   ├── __init__.py
│   ├── default_config.yaml    # 默认配置
│   └── voice_library.json     # 音色库配置
│
├── data/                      # 数据目录
│   ├── cache/                 # 缓存文件
│   ├── output/                # 输出文件
│   └── models/                # AI模型（可选）
│
├── tests/                     # 测试用例
│   ├── test_text_processor.py
│   ├── test_tts_engine.py
│   └── test_audio_processor.py
│
├── main.py                    # 主程序入口
├── requirements.txt           # 依赖包
├── README.md                  # 使用说明
└── PROJECT_DESIGN.md          # 本设计文档
```

---

## 技术栈

### 核心依赖

```python
# TTS引擎
pyttsx3==2.90              # 本地TTS
edge-tts==6.1.9            # Edge TTS
ChatTTS                    # 对话式TTS（可选）

# 云端TTS SDK
baidu-aip==4.16.13         # 百度AI
alibabacloud_nls20180518   # 阿里云
tencentcloud-sdk-python    # 腾讯云
openai>=1.0.0              # OpenAI（可选）

# 音频处理
pydub==0.25.1              # 音频处理
mutagen==1.47.0            # 元数据编辑
soundfile==0.12.1          # 音频文件读写
librosa==0.10.1            # 音频分析

# 文本处理
chardet==5.2.0             # 编码检测
jieba==0.42.1              # 中文分词
pypinyin==0.50.0           # 拼音转换

# AI/NLP（可选）
transformers>=4.35.0       # 情感分析
torch>=2.0.0               # 深度学习框架

# GUI界面
PyQt6==6.6.0               # 或 tkinter (内置)
# 或
customtkinter==5.2.1       # 现代化tkinter

# 工具库
loguru==0.7.2              # 日志
pyyaml==6.0.1              # 配置文件
python-dotenv==1.0.0       # 环境变量
tqdm==4.66.1               # 进度条
requests==2.32.5           # HTTP请求
```

---

## 实现路线图

### Phase 1: 基础功能（1-2周）
- [x] 项目架构搭建
- [ ] 文本导入和编码检测
- [ ] 基础TTS引擎集成（pyttsx3, edge-tts）
- [ ] 简单的命令行界面
- [ ] 基础音频导出

### Phase 2: 增强功能（2-3周）
- [ ] 章节智能识别
- [ ] 多音色支持
- [ ] 云端TTS集成（百度、阿里云、腾讯云）
- [ ] 图形界面开发
- [ ] 音频格式转换和质量优化

### Phase 3: AI功能（2-4周）
- [ ] 情感识别和表达
- [ ] 角色对话检测
- [ ] 多角色配音
- [ ] 背景音效系统
- [ ] 自动化场景识别

### Phase 4: 优化完善（1-2周）
- [ ] 性能优化（批处理、并发）
- [ ] 缓存机制
- [ ] 断点续传
- [ ] 完整的配置系统
- [ ] 用户手册和示例

---

## 核心算法流程

### 1. 文本处理流程
```
TXT文件 → 编码检测 → 文本清洗 → 章节识别 → 分段处理 → 语句优化 → TTS队列
```

### 2. TTS合成流程
```
文本段 → 选择引擎 → 选择音色 → 情感分析 → 语音合成 → 音频缓存 → 质量检查
```

### 3. 音频处理流程
```
原始音频 → 音量标准化 → 降噪处理 → 格式转换 → 添加元数据 → 章节合并 → 导出
```

### 4. AI增强流程
```
文本分析 → 角色识别 → 情感标注 → 音色分配 → 特效添加 → 背景音混音
```

---

## 配置文件示例

### default_config.yaml
```yaml
# TTS配置
tts:
  default_engine: "edge-tts"  # pyttsx3, edge-tts, baidu, aliyun, tencent
  default_voice: "zh-CN-XiaoxiaoNeural"
  speech_rate: 1.0
  volume: 1.0
  pitch: 1.0

# 音频配置
audio:
  format: "mp3"  # mp3, wav, m4a, m4b
  quality: "high"  # low, medium, high, lossless
  sample_rate: 44100
  bitrate: 192
  normalize: true

# 文本处理
text:
  encoding: "auto"  # auto, utf-8, gbk, gb2312
  chapter_pattern: "第[0-9零一二三四五六七八九十百千]+[章回节集]"
  max_segment_length: 500
  remove_annotations: true

# AI增强
ai:
  enable_emotion_detection: true
  enable_role_detection: true
  enable_multi_voice: true
  enable_background_music: false

# 缓存
cache:
  enable: true
  path: "./data/cache"
  max_size_mb: 1024
  auto_clean: true

# 云端API配置
cloud_api:
  baidu:
    app_id: ""
    api_key: ""
    secret_key: ""
  aliyun:
    access_key_id: ""
    access_key_secret: ""
  tencent:
    secret_id: ""
    secret_key: ""
```

---

## 使用场景

### 场景1: 快速转换
```bash
# 命令行方式
python main.py convert --input novel.txt --output audiobook.mp3 --voice xiaoxiao
```

### 场景2: 高质量有声书
```python
# 使用GUI选择：
# - 引擎：阿里云TTS
# - 音色：温柔女声
# - 启用AI增强
# - 添加背景音乐
# - 输出格式：M4B（带章节标记）
```

### 场景3: 多角色剧
```python
# 自动识别对话
# 主角：磁性男声
# 女主：甜美女声
# 旁白：播音腔
# 配角：智能分配
```

---

## 扩展功能规划

### 未来可添加的模块

1. **PDF/EPUB转有声书**
2. **网文爬虫 + 自动转换**
3. **字幕生成器（SRT/ASS）**
4. **视频制作工具（配合图片生成视频）**
5. **多语言翻译 + TTS**
6. **有声书播放器（内置）**
7. **批量处理工具**
8. **移动端APP（Kivy/Flutter）**

---

## 性能优化策略

1. **并发处理**: 多线程/多进程TTS合成
2. **缓存机制**: 相同文本复用音频
3. **增量更新**: 仅处理修改的章节
4. **流式处理**: 边合成边播放/保存
5. **GPU加速**: 使用GPU进行AI推理（如需要）

---

## 安全与隐私

1. **API密钥加密存储**
2. **本地处理优先**
3. **不上传用户文本到云端（除非必要）**
4. **缓存文件加密（可选）**

---

## 开发建议

### 开发优先级
1. 先实现基础流程（文本导入 → TTS → 音频导出）
2. 再添加多引擎支持
3. 最后实现AI增强功能

### 技术选型建议
- GUI: **PyQt6** (专业) 或 **CustomTkinter** (简单美观)
- TTS优先级: **edge-tts** (免费高质量) → **百度/阿里云** (商用)
- AI模型: 可选，初期可不集成

---

## 总结

这个项目完全可以实现！关键点：

1. **核心功能**: TXT导入 + TTS转换 + 音频导出 ✅
2. **多音色**: 支持本地和云端多种引擎 ✅
3. **AI效果**: 通过情感分析和多角色配音实现 ✅

**我可以立即开始帮你实现这个项目！**

你想先从哪个部分开始？
- A. 搭建基础架构 + 实现第一个TTS引擎
- B. 创建GUI界面框架
- C. 完整的命令行版本（CLI）
- D. 我有其他想法

请告诉我你的选择，我会立即开始编写代码！
