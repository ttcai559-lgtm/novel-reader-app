# Pytest 常用命令参考

## 基本运行

```bash
# 运行所有测试
pytest

# 运行指定目录
pytest testcases/

# 运行指定文件
pytest testcases/api/test_user.py

# 运行指定测试类
pytest testcases/api/test_user.py::TestUserLogin

# 运行指定测试方法
pytest testcases/api/test_user.py::TestUserLogin::test_login_success
```

## 输出控制

```bash
# 详细输出
pytest -v

# 显示print输出
pytest -s

# 组合使用
pytest -vs

# 简洁输出
pytest -q

# 只显示失败的用例
pytest --tb=short
```

## 标记运行

```bash
# 运行smoke测试
pytest -m smoke

# 运行多个标记
pytest -m "smoke or regression"

# 排除某些标记
pytest -m "not slow"

# 查看所有标记
pytest --markers
```

## 失败处理

```bash
# 遇到第一个失败就停止
pytest -x

# 遇到N个失败停止
pytest --maxfail=3

# 失败重试
pytest --reruns 2

# 只运行上次失败的用例
pytest --lf

# 先运行上次失败的，再运行其他
pytest --ff
```

## 并发运行

```bash
# 4个进程并发
pytest -n 4

# 自动检测CPU核心数
pytest -n auto
```

## 报告生成

```bash
# 生成HTML报告
pytest --html=report.html --self-contained-html

# 生成Allure报告
pytest --alluredir=./reports/allure-results

# 生成JUnit XML报告
pytest --junit-xml=report.xml
```

## 用例收集

```bash
# 只收集用例，不运行
pytest --collect-only

# 显示用例收集信息
pytest --collect-only -q
```

## 覆盖率

```bash
# 运行并生成覆盖率报告
pytest --cov=apis --cov-report=html

# 显示缺失的行
pytest --cov=apis --cov-report=term-missing
```

## 其他常用

```bash
# 显示最慢的10个用例
pytest --durations=10

# 设置超时时间（需要pytest-timeout）
pytest --timeout=60

# 调试模式
pytest --pdb

# 自定义环境
pytest --env=staging

# 使用自定义配置文件
pytest -c custom_pytest.ini
```

## 使用run_tests.py脚本

```bash
# 基本运行
python run_tests.py

# 指定环境
python run_tests.py --env=test

# 运行smoke测试
python run_tests.py -m smoke

# 指定路径
python run_tests.py -p testcases/api/test_user.py

# 并发运行
python run_tests.py -n 4

# 生成Allure报告
python run_tests.py --allure

# 生成并查看Allure报告
python run_tests.py --allure --serve

# 组合使用
python run_tests.py --env=test -m smoke -n 4 --allure
```

## CI/CD集成示例

```bash
# Jenkins/GitLab CI
pytest -v -s --html=report.html --alluredir=allure-results

# 带失败重试
pytest -v -s --reruns 2 --html=report.html
```
