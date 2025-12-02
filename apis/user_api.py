"""
用户相关API接口封装
示例：展示如何封装具体的API接口
"""
import allure
from apis.base_api import BaseAPI


class UserAPI(BaseAPI):
    """用户API接口类"""

    @allure.step("用户登录")
    def login(self, username: str, password: str):
        """
        用户登录接口
        :param username: 用户名
        :param password: 密码
        :return: Response对象
        """
        payload = {
            "username": username,
            "password": password
        }
        response = self.client.post("/api/v1/login", json_data=payload)
        return response

    @allure.step("获取用户信息")
    def get_user_info(self, user_id: int):
        """
        获取用户信息
        :param user_id: 用户ID
        :return: Response对象
        """
        response = self.client.get(f"/api/v1/users/{user_id}")
        return response

    @allure.step("创建用户")
    def create_user(self, username: str, email: str, password: str):
        """
        创建用户
        :param username: 用户名
        :param email: 邮箱
        :param password: 密码
        :return: Response对象
        """
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        response = self.client.post("/api/v1/users", json_data=payload)
        return response

    @allure.step("更新用户信息")
    def update_user(self, user_id: int, **kwargs):
        """
        更新用户信息
        :param user_id: 用户ID
        :param kwargs: 要更新的字段
        :return: Response对象
        """
        response = self.client.put(f"/api/v1/users/{user_id}", json_data=kwargs)
        return response

    @allure.step("删除用户")
    def delete_user(self, user_id: int):
        """
        删除用户
        :param user_id: 用户ID
        :return: Response对象
        """
        response = self.client.delete(f"/api/v1/users/{user_id}")
        return response

    @allure.step("获取用户列表")
    def get_user_list(self, page: int = 1, page_size: int = 10):
        """
        获取用户列表
        :param page: 页码
        :param page_size: 每页数量
        :return: Response对象
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        response = self.client.get("/api/v1/users", params=params)
        return response
