"""
断言工具类
提供丰富的断言方法，并自动记录到日志和Allure报告
"""
import allure
from typing import Any
from utils.logger import logger


class AssertUtil:
    """断言工具类"""

    @staticmethod
    def assert_equal(actual: Any, expected: Any, message: str = ""):
        """
        断言相等
        :param actual: 实际值
        :param expected: 期望值
        :param message: 断言消息
        """
        msg = message or f"断言相等失败: 期望值={expected}, 实际值={actual}"
        try:
            assert actual == expected, msg
            logger.info(f"断言通过: {message or '相等断言'} - 值={actual}")
            with allure.step(f"断言相等: 期望={expected}, 实际={actual}"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_not_equal(actual: Any, expected: Any, message: str = ""):
        """
        断言不相等
        :param actual: 实际值
        :param expected: 期望值
        :param message: 断言消息
        """
        msg = message or f"断言不相等失败: 实际值={actual} 等于 期望值={expected}"
        try:
            assert actual != expected, msg
            logger.info(f"断言通过: {message or '不相等断言'}")
            with allure.step(f"断言不相等: 实际={actual}, 不等于={expected}"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_in(member: Any, container: Any, message: str = ""):
        """
        断言包含
        :param member: 成员
        :param container: 容器
        :param message: 断言消息
        """
        msg = message or f"断言包含失败: {member} 不在 {container} 中"
        try:
            assert member in container, msg
            logger.info(f"断言通过: {message or '包含断言'}")
            with allure.step(f"断言包含: {member} 在容器中"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_not_in(member: Any, container: Any, message: str = ""):
        """
        断言不包含
        :param member: 成员
        :param container: 容器
        :param message: 断言消息
        """
        msg = message or f"断言不包含失败: {member} 在 {container} 中"
        try:
            assert member not in container, msg
            logger.info(f"断言通过: {message or '不包含断言'}")
            with allure.step(f"断言不包含: {member} 不在容器中"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_true(condition: bool, message: str = ""):
        """
        断言为真
        :param condition: 条件
        :param message: 断言消息
        """
        msg = message or f"断言为真失败: 条件={condition}"
        try:
            assert condition is True, msg
            logger.info(f"断言通过: {message or '为真断言'}")
            with allure.step(f"断言为真: {message or '条件为True'}"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_false(condition: bool, message: str = ""):
        """
        断言为假
        :param condition: 条件
        :param message: 断言消息
        """
        msg = message or f"断言为假失败: 条件={condition}"
        try:
            assert condition is False, msg
            logger.info(f"断言通过: {message or '为假断言'}")
            with allure.step(f"断言为假: {message or '条件为False'}"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_is_none(obj: Any, message: str = ""):
        """
        断言为None
        :param obj: 对象
        :param message: 断言消息
        """
        msg = message or f"断言为None失败: 对象={obj}"
        try:
            assert obj is None, msg
            logger.info(f"断言通过: {message or '为None断言'}")
            with allure.step(f"断言为None: {message or '对象为None'}"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_is_not_none(obj: Any, message: str = ""):
        """
        断言不为None
        :param obj: 对象
        :param message: 断言消息
        """
        msg = message or "断言不为None失败: 对象为None"
        try:
            assert obj is not None, msg
            logger.info(f"断言通过: {message or '不为None断言'}")
            with allure.step(f"断言不为None: {message or '对象不为None'}"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_status_code(response, expected_code: int, message: str = ""):
        """
        断言HTTP状态码
        :param response: Response对象
        :param expected_code: 期望状态码
        :param message: 断言消息
        """
        actual_code = response.status_code
        msg = message or f"状态码断言失败: 期望={expected_code}, 实际={actual_code}"
        try:
            assert actual_code == expected_code, msg
            logger.info(f"状态码断言通过: {actual_code}")
            with allure.step(f"断言状态码: 期望={expected_code}, 实际={actual_code}"):
                pass
        except AssertionError as e:
            logger.error(f"断言失败: {msg}")
            with allure.step(f"断言失败: {msg}"):
                pass
            raise e

    @staticmethod
    def assert_json_value(response, json_path: str, expected_value: Any, message: str = ""):
        """
        断言JSON响应中的值
        :param response: Response对象
        :param json_path: JSON路径（使用.分隔，如: data.user.name）
        :param expected_value: 期望值
        :param message: 断言消息
        """
        try:
            json_data = response.json()
            keys = json_path.split('.')
            actual_value = json_data

            for key in keys:
                if isinstance(actual_value, dict):
                    actual_value = actual_value.get(key)
                elif isinstance(actual_value, list):
                    actual_value = actual_value[int(key)]
                else:
                    raise KeyError(f"无法访问路径: {json_path}")

            msg = message or f"JSON值断言失败: 路径={json_path}, 期望={expected_value}, 实际={actual_value}"
            assert actual_value == expected_value, msg
            logger.info(f"JSON值断言通过: {json_path}={actual_value}")
            with allure.step(f"断言JSON值: {json_path}={expected_value}"):
                pass
        except Exception as e:
            logger.error(f"JSON值断言失败: {str(e)}")
            with allure.step(f"断言失败: {str(e)}"):
                pass
            raise e
