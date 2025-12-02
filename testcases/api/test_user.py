"""
用户接口测试用例
展示各种常见的测试场景和最佳实践
"""
import pytest
import allure
from utils.assert_util import AssertUtil


@allure.feature("用户模块")
@allure.story("用户登录")
class TestUserLogin:
    """用户登录测试类"""

    @allure.title("测试正常登录")
    @allure.description("使用正确的用户名和密码进行登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_success(self, user_api, config):
        """测试正常登录"""
        # 准备测试数据
        user_info = config.get_test_user("normal_user")

        # 执行登录
        with allure.step("发送登录请求"):
            response = user_api.login(
                username=user_info["username"],
                password=user_info["password"]
            )

        # 验证响应
        with allure.step("验证响应状态码"):
            AssertUtil.assert_status_code(response, 200)

        with allure.step("验证响应数据"):
            json_data = response.json()
            AssertUtil.assert_in("data", json_data, "响应中应包含data字段")
            AssertUtil.assert_in("token", json_data["data"], "data中应包含token字段")
            AssertUtil.assert_is_not_none(json_data["data"]["token"], "token不应为空")

    @allure.title("测试用户名错误登录")
    @allure.description("使用错误的用户名进行登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_with_wrong_username(self, user_api):
        """测试用户名错误"""
        response = user_api.login(
            username="wrong_username",
            password="any_password"
        )

        # 验证返回401或400
        assert response.status_code in [400, 401], "应返回认证失败状态码"

    @allure.title("测试密码错误登录")
    @allure.description("使用错误的密码进行登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_with_wrong_password(self, user_api, config):
        """测试密码错误"""
        user_info = config.get_test_user("normal_user")

        response = user_api.login(
            username=user_info["username"],
            password="wrong_password"
        )

        assert response.status_code in [400, 401], "应返回认证失败状态码"

    @allure.title("测试空用户名登录")
    @allure.description("用户名为空时登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.parametrize("username,password", [
        ("", "password123"),
        ("username", ""),
        ("", "")
    ])
    def test_login_with_empty_credentials(self, user_api, username, password):
        """测试空凭据"""
        response = user_api.login(username=username, password=password)
        assert response.status_code == 400, "应返回参数错误状态码"


@allure.feature("用户模块")
@allure.story("用户管理")
class TestUserManagement:
    """用户管理测试类"""

    @allure.title("测试获取用户信息")
    @allure.description("通过用户ID获取用户详细信息")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.user
    def test_get_user_info(self, user_api, login_user):
        """测试获取用户信息"""
        # 假设登录后可以获取当前用户ID
        user_id = 1

        response = user_api.get_user_info(user_id)

        AssertUtil.assert_status_code(response, 200)
        json_data = response.json()
        AssertUtil.assert_in("data", json_data)
        AssertUtil.assert_equal(json_data["data"]["id"], user_id)

    @allure.title("测试创建用户")
    @allure.description("创建新用户并验证返回结果")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.user
    def test_create_user(self, user_api, login_user):
        """测试创建用户"""
        response = user_api.create_user(
            username="test_user_001",
            email="test001@example.com",
            password="Test123456"
        )

        AssertUtil.assert_status_code(response, 201)
        json_data = response.json()
        AssertUtil.assert_in("data", json_data)
        AssertUtil.assert_equal(json_data["data"]["username"], "test_user_001")

    @allure.title("测试更新用户信息")
    @allure.description("更新用户信息并验证")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.user
    def test_update_user(self, user_api, login_user, create_test_user):
        """测试更新用户"""
        # 先创建一个用户
        create_response = create_test_user(
            username="user_to_update",
            email="update@example.com",
            password="Test123456"
        )
        user_id = create_response.json().get("data", {}).get("id")

        # 更新用户
        response = user_api.update_user(
            user_id=user_id,
            email="new_email@example.com"
        )

        AssertUtil.assert_status_code(response, 200)
        json_data = response.json()
        AssertUtil.assert_equal(json_data["data"]["email"], "new_email@example.com")

    @allure.title("测试删除用户")
    @allure.description("删除用户并验证")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.user
    def test_delete_user(self, user_api, login_user, create_test_user):
        """测试删除用户"""
        # 先创建一个用户
        create_response = create_test_user(
            username="user_to_delete",
            email="delete@example.com",
            password="Test123456"
        )
        user_id = create_response.json().get("data", {}).get("id")

        # 删除用户
        response = user_api.delete_user(user_id)
        AssertUtil.assert_status_code(response, 204)

    @allure.title("测试获取用户列表")
    @allure.description("获取用户列表并验证分页")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.user
    def test_get_user_list(self, user_api, login_user):
        """测试获取用户列表"""
        response = user_api.get_user_list(page=1, page_size=10)

        AssertUtil.assert_status_code(response, 200)
        json_data = response.json()
        AssertUtil.assert_in("data", json_data)
        AssertUtil.assert_in("items", json_data["data"])
        AssertUtil.assert_true(isinstance(json_data["data"]["items"], list))

    @allure.title("测试用户列表分页")
    @allure.description("验证不同分页参数")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.user
    @pytest.mark.parametrize("page,page_size", [
        (1, 10),
        (1, 20),
        (2, 10)
    ])
    def test_user_list_pagination(self, user_api, login_user, page, page_size):
        """测试用户列表分页"""
        response = user_api.get_user_list(page=page, page_size=page_size)

        AssertUtil.assert_status_code(response, 200)
        json_data = response.json()
        items = json_data["data"]["items"]
        assert len(items) <= page_size, f"返回数量不应超过{page_size}"
