"""
pytest 全局配置文件
定义全局 fixtures 和 hooks
"""
import os
import pytest
import allure
from datetime import datetime
from config.config import Config
from utils.logger import logger
from utils.http_client import HttpClient


@pytest.fixture(scope="session")
def config():
    """全局配置fixture"""
    return Config()


@pytest.fixture(scope="session")
def http_client(config):
    """HTTP客户端fixture"""
    client = HttpClient(base_url=config.BASE_URL, timeout=config.TIMEOUT)
    yield client
    client.close()


@pytest.fixture(scope="function")
def api_client(http_client):
    """每个测试用例独立的API客户端"""
    yield http_client


# ================== Hooks ==================

def pytest_configure(config):
    """pytest 启动时执行"""
    logger.info("=" * 100)
    logger.info("测试开始")
    logger.info(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 100)

    # 创建必要的目录
    os.makedirs("logs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)


def pytest_collection_modifyitems(session, config, items):
    """
    测试用例收集完成后，修改用例列表
    解决中文用例名称显示问题
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    获取每个用例的执行结果
    失败时自动截图（如果是UI测试）
    """
    outcome = yield
    report = outcome.get_result()

    # 设置report属性，用于fixture获取测试结果
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call":
        # 记录测试结果
        if report.passed:
            logger.info(f"测试通过: {item.name}")
        elif report.failed:
            logger.error(f"测试失败: {item.name}")
            logger.error(f"失败原因: {report.longreprtext}")
        elif report.skipped:
            logger.warning(f"测试跳过: {item.name}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """pytest 结束时执行"""
    logger.info("=" * 100)
    logger.info("测试结束")
    logger.info(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"总计: {terminalreporter._numcollected} 个用例")
    logger.info(f"通过: {len(terminalreporter.stats.get('passed', []))} 个")
    logger.info(f"失败: {len(terminalreporter.stats.get('failed', []))} 个")
    logger.info(f"跳过: {len(terminalreporter.stats.get('skipped', []))} 个")
    logger.info(f"错误: {len(terminalreporter.stats.get('error', []))} 个")
    logger.info("=" * 100)


# ================== 自定义命令行参数 ==================

def pytest_addoption(parser):
    """添加自定义命令行参数"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="运行环境: test, staging, prod"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="API基础URL"
    )


@pytest.fixture(scope="session")
def cmdopt_env(request):
    """获取环境参数"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def cmdopt_base_url(request):
    """获取base_url参数"""
    return request.config.getoption("--base-url")
