"""
HTTP客户端工具类
封装requests库，提供统一的HTTP请求接口
"""
import json
import time
import allure
import requests
from typing import Dict, Any, Optional, Union
from requests import Response, Session
from utils.logger import logger
from config.config import Config


class HttpClient:
    """HTTP客户端类"""

    def __init__(self, base_url: str = None, timeout: int = Config.TIMEOUT):
        """
        初始化HTTP客户端
        :param base_url: API基础URL
        :param timeout: 请求超时时间
        """
        self.base_url = base_url or Config.BASE_URL
        self.timeout = timeout
        self.session = Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "API-Test-Client/1.0"
        })

    def set_headers(self, headers: Dict[str, str]):
        """
        设置请求头
        :param headers: 请求头字典
        """
        self.session.headers.update(headers)

    def set_auth_token(self, token: str, token_type: str = "Bearer"):
        """
        设置认证token
        :param token: 认证token
        :param token_type: token类型
        """
        self.session.headers.update({
            "Authorization": f"{token_type} {token}"
        })

    def _build_url(self, path: str) -> str:
        """
        构建完整URL
        :param path: 接口路径
        :return: 完整URL
        """
        if path.startswith("http"):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求信息"""
        logger.info(f"[请求] {method.upper()} {url}")
        if kwargs.get("params"):
            logger.info(f"[请求参数] {kwargs['params']}")
        if kwargs.get("json"):
            logger.info(f"[请求体] {json.dumps(kwargs['json'], ensure_ascii=False, indent=2)}")
        if kwargs.get("data"):
            logger.info(f"[请求体] {kwargs['data']}")
        if kwargs.get("headers"):
            logger.info(f"[请求头] {kwargs['headers']}")

    def _log_response(self, response: Response):
        """记录响应信息"""
        logger.info(f"[响应状态] {response.status_code}")
        logger.info(f"[响应时间] {response.elapsed.total_seconds()}s")
        try:
            logger.info(f"[响应体] {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        except Exception:
            logger.info(f"[响应体] {response.text}")

    def _attach_to_allure(self, method: str, url: str, response: Response, **kwargs):
        """将请求和响应信息附加到Allure报告"""
        # 附加请求信息
        request_info = {
            "method": method.upper(),
            "url": url,
            "headers": dict(self.session.headers),
        }
        if kwargs.get("params"):
            request_info["params"] = kwargs["params"]
        if kwargs.get("json"):
            request_info["body"] = kwargs["json"]
        if kwargs.get("data"):
            request_info["body"] = kwargs["data"]

        allure.attach(
            json.dumps(request_info, ensure_ascii=False, indent=2),
            name="请求信息",
            attachment_type=allure.attachment_type.JSON
        )

        # 附加响应信息
        response_info = {
            "status_code": response.status_code,
            "elapsed": f"{response.elapsed.total_seconds()}s",
            "headers": dict(response.headers)
        }
        try:
            response_info["body"] = response.json()
        except Exception:
            response_info["body"] = response.text

        allure.attach(
            json.dumps(response_info, ensure_ascii=False, indent=2),
            name="响应信息",
            attachment_type=allure.attachment_type.JSON
        )

    def _request(
            self,
            method: str,
            path: str,
            retry: int = Config.RETRY_TIMES,
            **kwargs
    ) -> Response:
        """
        发送HTTP请求（支持重试）
        :param method: 请求方法
        :param path: 接口路径
        :param retry: 重试次数
        :param kwargs: 其他请求参数
        :return: Response对象
        """
        url = self._build_url(path)
        kwargs.setdefault("timeout", self.timeout)

        # 记录请求信息
        self._log_request(method, url, **kwargs)

        # 发送请求（支持重试）
        for i in range(retry):
            try:
                response = self.session.request(method, url, **kwargs)
                self._log_response(response)
                self._attach_to_allure(method, url, response, **kwargs)
                return response
            except requests.exceptions.RequestException as e:
                logger.error(f"[请求失败] 第{i + 1}次尝试失败: {str(e)}")
                if i == retry - 1:
                    raise
                time.sleep(Config.RETRY_DELAY)

    def get(self, path: str, params: Dict = None, **kwargs) -> Response:
        """
        发送GET请求
        :param path: 接口路径
        :param params: 查询参数
        :param kwargs: 其他请求参数
        :return: Response对象
        """
        return self._request("GET", path, params=params, **kwargs)

    def post(
            self,
            path: str,
            json_data: Dict = None,
            data: Any = None,
            **kwargs
    ) -> Response:
        """
        发送POST请求
        :param path: 接口路径
        :param json_data: JSON请求体
        :param data: 表单数据
        :param kwargs: 其他请求参数
        :return: Response对象
        """
        return self._request("POST", path, json=json_data, data=data, **kwargs)

    def put(
            self,
            path: str,
            json_data: Dict = None,
            data: Any = None,
            **kwargs
    ) -> Response:
        """
        发送PUT请求
        :param path: 接口路径
        :param json_data: JSON请求体
        :param data: 表单数据
        :param kwargs: 其他请求参数
        :return: Response对象
        """
        return self._request("PUT", path, json=json_data, data=data, **kwargs)

    def patch(
            self,
            path: str,
            json_data: Dict = None,
            data: Any = None,
            **kwargs
    ) -> Response:
        """
        发送PATCH请求
        :param path: 接口路径
        :param json_data: JSON请求体
        :param data: 表单数据
        :param kwargs: 其他请求参数
        :return: Response对象
        """
        return self._request("PATCH", path, json=json_data, data=data, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        """
        发送DELETE请求
        :param path: 接口路径
        :param kwargs: 其他请求参数
        :return: Response对象
        """
        return self._request("DELETE", path, **kwargs)

    def close(self):
        """关闭session"""
        self.session.close()
