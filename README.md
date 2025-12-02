# API 自动化测试框架

基于 Pytest 的专业接口自动化测试框架，提供完整的测试解决方案。

## 项目特点

- 基于 Pytest 测试框架，功能强大且易于扩展
- 完整的日志系统，自动记录请求和响应信息
- 支持 Allure 测试报告，可视化展示测试结果
- 封装 HTTP 客户端，支持请求重试和会话管理
- 支持多环境配置（测试、预发布、生产）
- 数据驱动测试，支持 JSON、YAML、CSV 格式
- 丰富的断言工具类，自动记录到日志和报告
- 支持数据库和 Redis 连接
- 提供测试数据自动清理机制
- 完善的 fixtures 体系，提高用例复用性

## 项目结构

```
tool_project/
├── apis/                   # API接口封装
│   ├── __init__.py
│   ├── base_api.py        # API基类
│   └── user_api.py        # 用户API示例
├── common/                 # 公共模块
│   ├── __init__.py
│   └── fixtures.py        # 公共fixtures
├── config/                 # 配置文件
│   ├── __init__.py
│   └── config.py          # 全局配置
├── data/                   # 测试数据
│   └── test_data/         # 测试数据文件
│       ├── user_data.json
│       └── api_test_data.yaml
├── logs/                   # 日志文件（自动生成）
├── reports/                # 测试报告（自动生成）
│   ├── allure-results/
│   └── screenshots/
├── testcases/              # 测试用例
│   ├── __init__.py
│   ├── conftest.py        # 测试用例fixtures
│   └── api/               # API测试用例
│       ├── __init__.py
│       └── test_user.py   # 用户接口测试示例
├── utils/                  # 工具类
│   ├── __init__.py
│   ├── assert_util.py     # 断言工具
│   ├── data_handler.py    # 数据处理工具
│   ├── db_client.py       # 数据库客户端
│   ├── http_client.py     # HTTP客户端
│   └── logger.py          # 日志工具
├── .env.example           # 环境变量示例
├── .gitignore             # Git忽略文件
├── conftest.py            # Pytest全局配置
├── pytest.ini             # Pytest配置文件
├── requirements.txt       # 项目依赖
└── README.md              # 项目说明文档
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目（如果使用Git）
git clone <repository-url>
cd tool_project

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑 .env 文件，填入实际配置
# 或者直接修改 config/config.py 中的配置
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定模块
pytest testcases/api/test_user.py

# 运行指定标记的用例
pytest -m smoke                    # 运行冒烟测试
pytest -m "login or user"          # 运行登录或用户相关用例

# 运行指定用例
pytest testcases/api/test_user.py::TestUserLogin::test_login_success

# 并发运行（需要安装pytest-xdist）
pytest -n 4                        # 4个进程并发

# 查看详细输出
pytest -v                          # 详细模式
pytest -s                          # 显示print输出
pytest -vs                         # 组合使用
```

### 4. 查看测试报告

```bash
# HTML报告（自动生成在 reports/report.html）
# 直接在浏览器中打开即可

# Allure报告
# 生成报告
allure generate reports/allure-results -o reports/allure-report --clean

# 查看报告
allure serve reports/allure-results
```

## 使用指南

### 编写测试用例

```python
import pytest
import allure
from utils.assert_util import AssertUtil


@allure.feature("用户模块")
@allure.story("用户登录")
class TestUserLogin:

    @allure.title("测试正常登录")
    @pytest.mark.smoke
    def test_login_success(self, user_api, config):
        # 获取测试数据
        user_info = config.get_test_user("normal_user")

        # 调用API
        response = user_api.login(
            username=user_info["username"],
            password=user_info["password"]
        )

        # 断言验证
        AssertUtil.assert_status_code(response, 200)
        AssertUtil.assert_in("token", response.json()["data"])
```

### 添加新的API接口

1. 在 `apis/` 目录下创建新的API文件
2. 继承 `BaseAPI` 类
3. 使用 `@allure.step` 装饰器标记步骤

```python
from apis.base_api import BaseAPI
import allure


class OrderAPI(BaseAPI):

    @allure.step("创建订单")
    def create_order(self, product_id: int, quantity: int):
        payload = {
            "product_id": product_id,
            "quantity": quantity
        }
        return self.client.post("/api/v1/orders", json_data=payload)
```

### 管理测试数据

支持三种格式的测试数据：

**JSON格式** (`data/test_data/xxx.json`)
```json
{
  "test_case_1": {
    "username": "test",
    "password": "123456"
  }
}
```

**YAML格式** (`data/test_data/xxx.yaml`)
```yaml
test_case_1:
  username: test
  password: 123456
```

**在用例中使用**
```python
def test_example(self, get_test_data):
    data = get_test_data("user_data.json", "test_case_1")
    # 使用data进行测试
```

### 使用数据库

```python
def test_with_database(self, db_connection):
    # 执行查询
    result = db_connection.execute_query(
        "SELECT * FROM users WHERE id = %s",
        (1,)
    )

    # 执行更新
    rows = db_connection.execute_update(
        "UPDATE users SET status = %s WHERE id = %s",
        ("active", 1)
    )
```

## 配置说明

### pytest.ini

- 定义测试文件、类、函数的命名规则
- 配置测试标记（markers）
- 设置日志格式和级别
- 配置Allure报告路径

### config/config.py

- 环境配置（测试、预发布、生产）
- API地址配置
- 数据库配置
- Redis配置
- 测试账号配置
- 文件路径配置

## 进阶功能

### 自定义Fixtures

在 `conftest.py` 中添加自定义fixtures：

```python
@pytest.fixture(scope="function")
def custom_fixture():
    # setup
    yield value
    # teardown
```

### 参数化测试

```python
@pytest.mark.parametrize("username,password,expected", [
    ("user1", "pass1", 200),
    ("user2", "pass2", 200),
    ("invalid", "wrong", 401),
])
def test_login(self, user_api, username, password, expected):
    response = user_api.login(username, password)
    assert response.status_code == expected
```

### 数据驱动

使用 `pytest-yaml` 或 `pytest-json` 实现数据驱动测试。

## 常见问题

### 1. 如何切换测试环境？

方法一：修改 `config/config.py` 中的 `ENV` 变量
```python
ENV = "staging"  # test, staging, prod
```

方法二：使用环境变量
```bash
export TEST_ENV=staging
pytest
```

方法三：使用命令行参数
```bash
pytest --env=staging
```

### 2. 如何跳过某些测试？

```python
@pytest.mark.skip(reason="暂时跳过")
def test_example():
    pass

@pytest.mark.skipif(condition, reason="条件跳过")
def test_example2():
    pass
```

### 3. 如何处理认证token？

框架已内置token管理：

```python
# 登录后自动设置token
response = user_api.login(username, password)
token = response.json()["data"]["token"]
user_api.client.set_auth_token(token)

# 或使用login_user fixture自动登录
def test_with_auth(self, user_api, login_user):
    # login_user会自动登录并设置token
    pass
```

## 最佳实践

1. **用例设计原则**
   - 每个测试用例只测试一个功能点
   - 用例之间保持独立，不要相互依赖
   - 使用有意义的用例名称和描述

2. **数据管理**
   - 测试数据与测试代码分离
   - 使用fixtures自动清理测试数据
   - 敏感数据使用环境变量

3. **断言规范**
   - 使用 `AssertUtil` 进行断言，自动记录日志
   - 断言失败时提供清晰的错误信息
   - 对关键字段进行多重断言

4. **日志记录**
   - 关键步骤使用 `@allure.step` 标记
   - 重要信息使用logger记录
   - 失败时自动记录详细信息

## 维护与扩展

- 定期更新依赖包版本
- 根据项目需求扩展工具类
- 完善测试数据和用例覆盖
- 优化CI/CD集成

## 联系方式

如有问题或建议，请联系测试团队。

## 更新日志

### v1.0.0 (2025-11-24)
- 初始版本发布
- 完整的pytest测试框架
- HTTP客户端封装
- 日志和报告系统
- 数据库支持
- 示例测试用例
