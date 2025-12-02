"""
文本处理器
整合编码检测、文本清洗、章节解析等功能
"""
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger

from .encoding_detector import EncodingDetector
from .text_cleaner import TextCleaner
from .chapter_parser import ChapterParser, Chapter


class TextProcessor:
    """文本处理器 - 统一处理小说文本的入口"""

    def __init__(
        self,
        encoding: Optional[str] = None,
        remove_annotations: bool = True,
        remove_ads: bool = True,
        custom_chapter_pattern: Optional[str] = None,
        max_segment_length: int = 500
    ):
        """
        初始化文本处理器

        Args:
            encoding: 指定编码，None则自动检测
            remove_annotations: 是否移除注释
            remove_ads: 是否移除广告
            custom_chapter_pattern: 自定义章节模式
            max_segment_length: 最大段落长度（字符数）
        """
        self.encoding = encoding
        self.max_segment_length = max_segment_length

        # 初始化子模块
        self.encoding_detector = EncodingDetector()
        self.text_cleaner = TextCleaner(
            remove_annotations=remove_annotations,
            remove_ads=remove_ads
        )
        self.chapter_parser = ChapterParser(custom_pattern=custom_chapter_pattern)

    def load_novel(self, file_path: str) -> Dict:
        """
        加载小说文件并完整处理

        Args:
            file_path: 小说文件路径

        Returns:
            处理结果字典，包含：
            - raw_text: 原始文本
            - cleaned_text: 清洗后文本
            - chapters: 章节列表
            - summary: 统计信息
        """
        logger.info(f"开始加载小说: {file_path}")

        # 1. 读取文件（自动检测编码）
        raw_text = self.encoding_detector.read_file_with_encoding(
            file_path,
            encoding=self.encoding
        )
        logger.info(f"文件读取完成，共 {len(raw_text)} 字符")

        # 2. 清洗文本
        cleaned_text = self.text_cleaner.clean(raw_text)

        # 3. 解析章节
        chapters = self.chapter_parser.parse(cleaned_text)

        # 4. 生成统计信息
        summary = self._generate_summary(raw_text, cleaned_text, chapters)

        logger.success(f"小说加载完成: {summary['total_chapters']} 章, {summary['total_characters']} 字")

        return {
            'file_path': str(Path(file_path).absolute()),
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'chapters': chapters,
            'summary': summary
        }

    def split_long_chapter(self, chapter: Chapter) -> List[Dict]:
        """
        将过长的章节分割成多个段落

        Args:
            chapter: 章节对象

        Returns:
            段落列表，每个段落包含 {text, index}
        """
        content = chapter.content
        segments = []

        # 先按自然段落分割
        paragraphs = self.text_cleaner.split_paragraphs(content)

        current_segment = ""
        segment_index = 0

        for para in paragraphs:
            # 如果单个段落就超过限制，需要强制分割
            if len(para) > self.max_segment_length:
                # 先保存当前累积的段落
                if current_segment:
                    segments.append({
                        'text': current_segment.strip(),
                        'index': segment_index,
                        'chapter_title': chapter.title
                    })
                    segment_index += 1
                    current_segment = ""

                # 分割超长段落
                for i in range(0, len(para), self.max_segment_length):
                    segments.append({
                        'text': para[i:i + self.max_segment_length],
                        'index': segment_index,
                        'chapter_title': chapter.title
                    })
                    segment_index += 1
            else:
                # 检查加上这个段落是否会超限
                if len(current_segment) + len(para) + 1 > self.max_segment_length:
                    # 保存当前段落，开始新段落
                    if current_segment:
                        segments.append({
                            'text': current_segment.strip(),
                            'index': segment_index,
                            'chapter_title': chapter.title
                        })
                        segment_index += 1
                    current_segment = para
                else:
                    # 累积段落
                    current_segment += "\n" + para if current_segment else para

        # 保存最后的段落
        if current_segment:
            segments.append({
                'text': current_segment.strip(),
                'index': segment_index,
                'chapter_title': chapter.title
            })

        logger.info(f"章节 '{chapter.title}' 分割为 {len(segments)} 个段落")
        return segments

    def prepare_for_tts(self, chapters: List[Chapter]) -> List[Dict]:
        """
        准备用于TTS的文本段落列表

        Args:
            chapters: 章节列表

        Returns:
            TTS任务列表，每个任务包含：
            - chapter_index: 章节序号
            - chapter_title: 章节标题
            - segment_index: 段落序号
            - text: 文本内容
            - task_id: 唯一任务ID
        """
        tts_tasks = []
        task_id = 0

        for chapter in chapters:
            segments = self.split_long_chapter(chapter)

            for seg in segments:
                tts_tasks.append({
                    'task_id': task_id,
                    'chapter_index': chapter.index,
                    'chapter_title': chapter.title,
                    'segment_index': seg['index'],
                    'text': seg['text'],
                    'char_count': len(seg['text'])
                })
                task_id += 1

        logger.info(f"生成 {len(tts_tasks)} 个TTS任务")
        return tts_tasks

    def _generate_summary(self, raw_text: str, cleaned_text: str, chapters: List[Chapter]) -> Dict:
        """
        生成统计信息

        Args:
            raw_text: 原始文本
            cleaned_text: 清洗后文本
            chapters: 章节列表

        Returns:
            统计信息字典
        """
        return {
            'raw_length': len(raw_text),
            'cleaned_length': len(cleaned_text),
            'removed_chars': len(raw_text) - len(cleaned_text),
            'total_chapters': len(chapters),
            'total_characters': sum(len(ch.content) for ch in chapters),
            'average_chapter_length': sum(len(ch.content) for ch in chapters) // len(chapters) if chapters else 0,
            'chapters_info': [
                {
                    'index': ch.index,
                    'title': ch.title,
                    'length': len(ch.content)
                }
                for ch in chapters
            ]
        }


if __name__ == '__main__':
    # 测试代码
    processor = TextProcessor()

    # 示例：处理小说文件
    # result = processor.load_novel("test_novel.txt")
    #
    # print(f"章节数: {result['summary']['total_chapters']}")
    # print(f"总字数: {result['summary']['total_characters']}")
    #
    # # 准备TTS任务
    # tts_tasks = processor.prepare_for_tts(result['chapters'])
    # print(f"TTS任务数: {len(tts_tasks)}")
    # print(f"第一个任务: {tts_tasks[0]}")
