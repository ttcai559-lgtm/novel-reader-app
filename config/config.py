"""
全局配置管理
支持多环境配置
"""
import os
from typing import Dict, Any


class Config:
    """配置类 - 管理所有测试配置"""

    # ================== 环境配置 ==================
    ENV = os.getenv("TEST_ENV", "test")  # test, staging, prod

    # ================== API配置 ==================
    # 多环境URL配置
    ENV_URLS = {
        "test": "http://test-api.example.com",
        "staging": "http://staging-api.example.com",
        "prod": "http://api.example.com"
    }

    BASE_URL = os.getenv("BASE_URL", ENV_URLS.get(ENV, ENV_URLS["test"]))

    # 请求超时配置
    TIMEOUT = 30
    RETRY_TIMES = 3
    RETRY_DELAY = 1

    # ================== 数据库配置 ==================
    DB_CONFIG = {
        "test": {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "password",
            "database": "test_db"
        },
        "staging": {
            "host": "staging-db.example.com",
            "port": 3306,
            "user": "staging_user",
            "password": "staging_pass",
            "database": "staging_db"
        },
        "prod": {
            "host": "prod-db.example.com",
            "port": 3306,
            "user": "prod_user",
            "password": "prod_pass",
            "database": "prod_db"
        }
    }

    # ================== Redis配置 ==================
    REDIS_CONFIG = {
        "test": {
            "host": "localhost",
            "port": 6379,
            "db": 0,
            "password": None
        },
        "staging": {
            "host": "staging-redis.example.com",
            "port": 6379,
            "db": 0,
            "password": "staging_redis_pass"
        }
    }

    # ================== 认证配置 ==================
    # 测试账号配置
    TEST_USERS = {
        "admin": {
            "username": "admin",
            "password": "admin123"
        },
        "normal_user": {
            "username": "test_user",
            "password": "test123"
        }
    }

    # ================== 文件路径配置 ==================
    # 项目根目录
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 数据目录
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    TEST_DATA_DIR = os.path.join(DATA_DIR, "test_data")

    # 日志目录
    LOG_DIR = os.path.join(ROOT_DIR, "logs")

    # 报告目录
    REPORT_DIR = os.path.join(ROOT_DIR, "reports")
    ALLURE_RESULTS_DIR = os.path.join(REPORT_DIR, "allure-results")
    SCREENSHOT_DIR = os.path.join(REPORT_DIR, "screenshots")

    # ================== 日志配置 ==================
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # ================== 其他配置 ==================
    # 是否开启Mock数据
    ENABLE_MOCK = False

    # 是否开启数据库校验
    ENABLE_DB_VERIFY = True

    # 是否开启截图
    ENABLE_SCREENSHOT = True

    @classmethod
    def get_db_config(cls) -> Dict[str, Any]:
        """获取当前环境的数据库配置"""
        return cls.DB_CONFIG.get(cls.ENV, cls.DB_CONFIG["test"])

    @classmethod
    def get_redis_config(cls) -> Dict[str, Any]:
        """获取当前环境的Redis配置"""
        return cls.REDIS_CONFIG.get(cls.ENV, cls.REDIS_CONFIG["test"])

    @classmethod
    def get_test_user(cls, user_type: str = "normal_user") -> Dict[str, str]:
        """获取测试用户信息"""
        return cls.TEST_USERS.get(user_type, cls.TEST_USERS["normal_user"])
