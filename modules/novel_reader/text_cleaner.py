"""
文本清洗器
清理小说文本中的无用内容和格式化文本
"""
import re
from typing import List
from loguru import logger


class TextCleaner:
    """文本清洗器"""

    # 常见需要清理的模式
    PATTERNS = {
        # 广告和版权声明
        'ads': r'(本书由.*?提供|.*?首发|.*?更新最快|.*?无弹窗|.*?免费阅读)',
        # 网址
        'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        # 多余的空白字符
        'multi_newline': r'\n{3,}',
        'multi_space': r' {2,}',
        # 特殊符号
        'special_chars': r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]',
    }

    def __init__(self, remove_annotations: bool = True, remove_ads: bool = True):
        """
        初始化文本清洗器

        Args:
            remove_annotations: 是否移除注释和说明
            remove_ads: 是否移除广告
        """
        self.remove_annotations = remove_annotations
        self.remove_ads = remove_ads

    def clean(self, text: str) -> str:
        """
        清洗文本

        Args:
            text: 原始文本

        Returns:
            清洗后的文本
        """
        if not text:
            return ""

        original_length = len(text)
        logger.info(f"开始清洗文本，原始长度: {original_length} 字符")

        # 移除特殊控制字符
        text = re.sub(self.PATTERNS['special_chars'], '', text)

        # 移除广告
        if self.remove_ads:
            text = re.sub(self.PATTERNS['ads'], '', text, flags=re.IGNORECASE)

        # 移除网址
        text = re.sub(self.PATTERNS['url'], '', text)

        # 移除注释（括号内的说明）
        if self.remove_annotations:
            text = self._remove_annotations(text)

        # 规范化空白字符
        text = self._normalize_whitespace(text)

        cleaned_length = len(text)
        logger.success(f"文本清洗完成，清理了 {original_length - cleaned_length} 字符")

        return text

    def _remove_annotations(self, text: str) -> str:
        """
        移除注释和说明

        Args:
            text: 文本

        Returns:
            移除注释后的文本
        """
        # 移除【】内的注释
        text = re.sub(r'【[^】]*】', '', text)
        # 移除小括号内的简短注释（少于20字）
        text = re.sub(r'\([^)]{1,20}\)', lambda m: '' if self._is_annotation(m.group()) else m.group(), text)

        return text

    @staticmethod
    def _is_annotation(text: str) -> bool:
        """
        判断是否为注释

        Args:
            text: 文本片段

        Returns:
            是否为注释
        """
        # 简单判断：如果包含"注"、"说明"等关键词
        keywords = ['注', '说明', '作者', 'PS', 'ps']
        return any(keyword in text for keyword in keywords)

    def _normalize_whitespace(self, text: str) -> str:
        """
        规范化空白字符

        Args:
            text: 文本

        Returns:
            规范化后的文本
        """
        # 替换多个换行为两个
        text = re.sub(self.PATTERNS['multi_newline'], '\n\n', text)
        # 替换多个空格为一个
        text = re.sub(self.PATTERNS['multi_space'], ' ', text)
        # 移除行首行尾空白
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        return text

    def split_paragraphs(self, text: str) -> List[str]:
        """
        将文本分割成段落

        Args:
            text: 文本

        Returns:
            段落列表
        """
        # 按换行符分割
        paragraphs = text.split('\n')
        # 过滤空段落
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        logger.info(f"文本分割为 {len(paragraphs)} 个段落")
        return paragraphs


if __name__ == '__main__':
    # 测试代码
    cleaner = TextCleaner()

    test_text = """
    第一章 开始

    这是一个测试文本【作者注：这是注释】。

    本书由某某网站首发，更新最快。

    主角说："你好！"（这是一个说明）



    这里有多余的空行。
    """

    cleaned = cleaner.clean(test_text)
    print("清洗后的文本：")
    print(cleaned)
    print("\n段落分割：")
    paragraphs = cleaner.split_paragraphs(cleaned)
    for i, p in enumerate(paragraphs, 1):
        print(f"{i}. {p}")
