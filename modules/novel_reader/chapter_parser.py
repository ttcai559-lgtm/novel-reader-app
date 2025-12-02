"""
章节解析器
智能识别和分割小说章节
"""
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class Chapter:
    """章节数据类"""
    title: str  # 章节标题
    content: str  # 章节内容
    index: int  # 章节序号
    start_pos: int  # 起始位置
    end_pos: int  # 结束位置


class ChapterParser:
    """章节解析器"""

    # 章节标题的常见模式
    CHAPTER_PATTERNS = [
        r'^第[0-9零一二三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬]+[章回节集部篇卷]\s*.{0,30}$',  # 第X章
        r'^[0-9]+[章回节集部篇卷]\s*.{0,30}$',  # 1章
        r'^Chapter\s*[0-9IVXivx]+.*$',  # Chapter 1
        r'^\s*[0-9]{1,4}\s*.{0,30}$',  # 纯数字章节
        r'^[【\[]第[0-9零一二三四五六七八九十百千]+[章回节集][】\]]\s*.{0,30}$',  # 【第X章】
    ]

    def __init__(self, custom_pattern: Optional[str] = None):
        """
        初始化章节解析器

        Args:
            custom_pattern: 自定义章节匹配模式（正则表达式）
        """
        self.patterns = self.CHAPTER_PATTERNS.copy()
        if custom_pattern:
            self.patterns.insert(0, custom_pattern)

        # 编译正则表达式
        self.compiled_patterns = [re.compile(p, re.MULTILINE) for p in self.patterns]

    def parse(self, text: str) -> List[Chapter]:
        """
        解析文本，提取章节

        Args:
            text: 小说全文

        Returns:
            章节列表
        """
        logger.info("开始解析章节...")

        # 查找所有章节标题
        chapter_positions = self._find_chapter_positions(text)

        if not chapter_positions:
            logger.warning("未找到章节标记，将整个文本作为单章节")
            return [Chapter(
                title="全文",
                content=text,
                index=1,
                start_pos=0,
                end_pos=len(text)
            )]

        # 提取章节内容
        chapters = self._extract_chapters(text, chapter_positions)

        logger.success(f"成功解析 {len(chapters)} 个章节")
        return chapters

    def _find_chapter_positions(self, text: str) -> List[Dict]:
        """
        查找所有章节标题位置

        Args:
            text: 文本

        Returns:
            章节位置信息列表 [{title, start, end}, ...]
        """
        positions = []
        lines = text.split('\n')
        current_pos = 0

        for line_num, line in enumerate(lines):
            line_stripped = line.strip()

            # 跳过空行和过长的行（可能不是标题）
            if not line_stripped or len(line_stripped) > 50:
                current_pos += len(line) + 1
                continue

            # 检查是否匹配章节模式
            if self._is_chapter_title(line_stripped):
                positions.append({
                    'title': line_stripped,
                    'start': current_pos,
                    'line_num': line_num
                })

            current_pos += len(line) + 1

        return positions

    def _is_chapter_title(self, line: str) -> bool:
        """
        判断是否为章节标题

        Args:
            line: 文本行

        Returns:
            是否为章节标题
        """
        for pattern in self.compiled_patterns:
            if pattern.match(line):
                return True
        return False

    def _extract_chapters(self, text: str, positions: List[Dict]) -> List[Chapter]:
        """
        根据位置信息提取章节内容

        Args:
            text: 全文
            positions: 章节位置列表

        Returns:
            章节列表
        """
        chapters = []

        for i, pos in enumerate(positions):
            # 确定章节内容的起止位置
            start = pos['start']
            end = positions[i + 1]['start'] if i + 1 < len(positions) else len(text)

            # 提取内容（去除标题行）
            chapter_text = text[start:end]
            lines = chapter_text.split('\n')
            title = lines[0].strip()
            content = '\n'.join(lines[1:]).strip()

            # 过滤过短的章节（可能是误识别）
            if len(content) < 50:
                logger.warning(f"章节 '{title}' 内容过短({len(content)}字符)，可能识别有误")

            chapters.append(Chapter(
                title=title,
                content=content,
                index=i + 1,
                start_pos=start,
                end_pos=end
            ))

        return chapters

    def get_chapter_summary(self, chapters: List[Chapter]) -> Dict:
        """
        获取章节统计信息

        Args:
            chapters: 章节列表

        Returns:
            统计信息字典
        """
        total_chars = sum(len(ch.content) for ch in chapters)
        avg_length = total_chars // len(chapters) if chapters else 0

        summary = {
            'total_chapters': len(chapters),
            'total_characters': total_chars,
            'average_length': avg_length,
            'chapters': [
                {
                    'index': ch.index,
                    'title': ch.title,
                    'length': len(ch.content)
                }
                for ch in chapters
            ]
        }

        return summary


if __name__ == '__main__':
    # 测试代码
    parser = ChapterParser()

    test_text = """
    第一章 开始的地方

    这是第一章的内容。
    主角在这里开始了他的冒险。

    第二章 新的挑战

    第二章的内容在这里。
    故事情节继续发展。

    第三章 转折点

    第三章内容...
    """

    chapters = parser.parse(test_text)
    print(f"找到 {len(chapters)} 个章节:\n")

    for ch in chapters:
        print(f"章节 {ch.index}: {ch.title}")
        print(f"内容长度: {len(ch.content)} 字符")
        print(f"内容预览: {ch.content[:50]}...")
        print("-" * 50)

    # 统计信息
    summary = parser.get_chapter_summary(chapters)
    print(f"\n统计信息:")
    print(f"总章节数: {summary['total_chapters']}")
    print(f"总字符数: {summary['total_characters']}")
    print(f"平均长度: {summary['average_length']}")
