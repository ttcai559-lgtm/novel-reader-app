"""
日志工具类
提供统一的日志记录功能
"""
import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from config.config import Config


class Logger:
    """日志类"""

    def __init__(self, name: str = __name__, level: str = Config.LOG_LEVEL):
        """
        初始化日志器
        :param name: 日志器名称
        :param level: 日志级别
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """配置日志处理器"""
        # 确保日志目录存在
        os.makedirs(Config.LOG_DIR, exist_ok=True)

        # 创建格式化器
        formatter = logging.Formatter(
            Config.LOG_FORMAT,
            datefmt=Config.LOG_DATE_FORMAT
        )

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # 文件处理器 - 所有日志
        log_file = os.path.join(
            Config.LOG_DIR,
            f"test_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # 错误日志处理器
        error_log_file = os.path.join(
            Config.LOG_DIR,
            f"error_{datetime.now().strftime('%Y%m%d')}.log"
        )
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)

    def debug(self, message: str):
        """调试日志"""
        self.logger.debug(message)

    def info(self, message: str):
        """信息日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """警告日志"""
        self.logger.warning(message)

    def error(self, message: str):
        """错误日志"""
        self.logger.error(message)

    def critical(self, message: str):
        """严重错误日志"""
        self.logger.critical(message)


# 创建全局logger实例
logger = Logger(name="API_TEST").logger
