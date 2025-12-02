"""
API基类
所有API接口类的父类，提供通用方法
"""
from utils.http_client import HttpClient
from utils.assert_util import AssertUtil


class BaseAPI:
    """API基类"""

    def __init__(self, http_client: HttpClient):
        """
        初始化API基类
        :param http_client: HTTP客户端实例
        """
        self.client = http_client
        self.assert_util = AssertUtil()

    def verify_response_success(self, response, expected_code: int = 200):
        """
        验证响应成功
        :param response: 响应对象
        :param expected_code: 期望状态码
        """
        self.assert_util.assert_status_code(response, expected_code)

    def get_response_data(self, response, data_key: str = "data"):
        """
        获取响应数据
        :param response: 响应对象
        :param data_key: 数据字段key
        :return: 数据
        """
        json_data = response.json()
        return json_data.get(data_key)
