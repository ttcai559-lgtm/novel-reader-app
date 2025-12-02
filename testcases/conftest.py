"""
测试用例级别的conftest
定义测试用例专用的fixtures
"""
import pytest
from apis.user_api import UserAPI


@pytest.fixture(scope="function")
def user_api(api_client):
    """用户API接口fixture"""
    return UserAPI(api_client)


@pytest.fixture(scope="function")
def login_user(user_api, config):
    """
    登录用户fixture
    自动登录并返回token
    """
    user_info = config.get_test_user("normal_user")
    response = user_api.login(
        username=user_info["username"],
        password=user_info["password"]
    )
    assert response.status_code == 200, "登录失败"

    token = response.json().get("data", {}).get("token")
    if token:
        user_api.client.set_auth_token(token)

    yield {
        "token": token,
        "user_info": user_info,
        "response": response
    }


@pytest.fixture(scope="function")
def create_test_user(user_api):
    """
    创建测试用户fixture
    测试完成后自动清理
    """
    created_users = []

    def _create_user(username: str, email: str, password: str):
        """创建用户并记录"""
        response = user_api.create_user(username, email, password)
        if response.status_code == 201:
            user_id = response.json().get("data", {}).get("id")
            created_users.append(user_id)
        return response

    yield _create_user

    # 清理：删除创建的用户
    for user_id in created_users:
        try:
            user_api.delete_user(user_id)
        except Exception as e:
            print(f"清理用户失败: {user_id}, 错误: {str(e)}")
