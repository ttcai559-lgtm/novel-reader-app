"""
公共fixtures
可以被所有测试用例使用的通用fixtures
"""
import pytest
from typing import Dict, Any
from utils.data_handler import TestDataManager
from config.config import Config


@pytest.fixture(scope="session")
def test_data_loader():
    """
    测试数据加载器fixture
    返回一个可以加载测试数据的函数
    """
    return TestDataManager()


@pytest.fixture(scope="function")
def get_test_data(test_data_loader):
    """
    获取测试数据fixture
    用法: test_data = get_test_data("user_data.json", "login_success")
    """
    def _get_data(file_name: str, case_name: str = None) -> Any:
        data = test_data_loader.load_test_data(file_name)
        if case_name:
            return data.get(case_name)
        return data

    return _get_data


@pytest.fixture(scope="session")
def db_connection():
    """
    数据库连接fixture
    自动管理数据库连接的生命周期
    """
    from utils.db_client import MySQLClient

    db_config = Config.get_db_config()
    db_client = MySQLClient(**db_config)
    db_client.connect()

    yield db_client

    db_client.close()


@pytest.fixture(scope="session")
def redis_connection():
    """
    Redis连接fixture
    自动管理Redis连接的生命周期
    """
    from utils.db_client import RedisClient

    redis_config = Config.get_redis_config()
    redis_client = RedisClient(**redis_config)
    redis_client.connect()

    yield redis_client

    redis_client.close()


@pytest.fixture(scope="function")
def cleanup_data():
    """
    数据清理fixture
    用于在测试后清理产生的测试数据
    """
    cleanup_actions = []

    def _add_cleanup(action, *args, **kwargs):
        """添加清理动作"""
        cleanup_actions.append((action, args, kwargs))

    yield _add_cleanup

    # 执行清理动作
    for action, args, kwargs in cleanup_actions:
        try:
            action(*args, **kwargs)
        except Exception as e:
            print(f"清理数据失败: {str(e)}")


@pytest.fixture(scope="function")
def mock_data():
    """
    Mock数据fixture
    用于提供模拟数据
    """
    return {
        "user": {
            "id": 1,
            "username": "mock_user",
            "email": "mock@example.com"
        },
        "token": "mock_token_123456",
        "response_success": {
            "code": 0,
            "message": "success",
            "data": {}
        },
        "response_error": {
            "code": -1,
            "message": "error",
            "data": None
        }
    }
