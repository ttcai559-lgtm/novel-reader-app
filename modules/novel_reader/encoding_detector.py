"""
文本编码检测器
支持自动检测中文常见编码：UTF-8, GBK, GB2312, GB18030等
"""
import chardet
from pathlib import Path
from typing import Dict, Optional
from loguru import logger


class EncodingDetector:
    """文本编码检测器"""

    # 常见中文编码优先级
    COMMON_ENCODINGS = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'utf-16', 'big5']

    @staticmethod
    def detect_file_encoding(file_path: str, sample_size: int = 100000) -> Dict[str, any]:
        """
        检测文件编码

        Args:
            file_path: 文件路径
            sample_size: 采样大小（字节），默认100KB

        Returns:
            Dict包含: encoding, confidence, language
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")

            # 读取文件样本
            with open(file_path, 'rb') as f:
                raw_data = f.read(sample_size)

            # 使用chardet检测
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']

            logger.info(f"检测到编码: {encoding}, 置信度: {confidence:.2%}")

            # 如果置信度较低，尝试常见编码
            if confidence < 0.7:
                logger.warning(f"置信度较低，尝试常见中文编码...")
                encoding = EncodingDetector._try_common_encodings(raw_data)

            return {
                'encoding': encoding,
                'confidence': confidence,
                'language': result.get('language', 'unknown')
            }

        except Exception as e:
            logger.error(f"编码检测失败: {e}")
            raise

    @staticmethod
    def _try_common_encodings(raw_data: bytes) -> str:
        """
        尝试使用常见编码解码

        Args:
            raw_data: 原始字节数据

        Returns:
            最佳编码名称
        """
        for encoding in EncodingDetector.COMMON_ENCODINGS:
            try:
                raw_data.decode(encoding)
                logger.info(f"成功使用编码: {encoding}")
                return encoding
            except (UnicodeDecodeError, LookupError):
                continue

        # 如果都失败，返回utf-8并忽略错误
        logger.warning("无法确定编码，默认使用 utf-8")
        return 'utf-8'

    @staticmethod
    def read_file_with_encoding(file_path: str, encoding: Optional[str] = None) -> str:
        """
        使用指定或自动检测的编码读取文件

        Args:
            file_path: 文件路径
            encoding: 指定编码，None则自动检测

        Returns:
            文件内容字符串
        """
        try:
            # 如果未指定编码，自动检测
            if encoding is None:
                detection_result = EncodingDetector.detect_file_encoding(file_path)
                encoding = detection_result['encoding']

            # 读取文件
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()

            logger.success(f"成功读取文件: {file_path} (编码: {encoding})")
            return content

        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            raise


if __name__ == '__main__':
    # 测试代码
    detector = EncodingDetector()

    # 示例：检测编码
    # result = detector.detect_file_encoding("test_novel.txt")
    # print(f"编码: {result['encoding']}, 置信度: {result['confidence']:.2%}")

    # 示例：读取文件
    # content = detector.read_file_with_encoding("test_novel.txt")
    # print(f"文件长度: {len(content)} 字符")
