"""
数据处理工具类
包括JSON、YAML、Excel等数据文件的读写
"""
import json
import yaml
import csv
import os
from typing import Any, Dict, List, Union
from config.config import Config
from utils.logger import logger


class DataHandler:
    """数据处理类"""

    @staticmethod
    def read_json(file_path: str) -> Union[Dict, List]:
        """
        读取JSON文件
        :param file_path: 文件路径
        :return: JSON数据
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"读取JSON文件成功: {file_path}")
            return data
        except Exception as e:
            logger.error(f"读取JSON文件失败: {file_path}, 错误: {str(e)}")
            raise

    @staticmethod
    def write_json(file_path: str, data: Union[Dict, List], indent: int = 2):
        """
        写入JSON文件
        :param file_path: 文件路径
        :param data: 要写入的数据
        :param indent: 缩进空格数
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            logger.info(f"写入JSON文件成功: {file_path}")
        except Exception as e:
            logger.error(f"写入JSON文件失败: {file_path}, 错误: {str(e)}")
            raise

    @staticmethod
    def read_yaml(file_path: str) -> Union[Dict, List]:
        """
        读取YAML文件
        :param file_path: 文件路径
        :return: YAML数据
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            logger.info(f"读取YAML文件成功: {file_path}")
            return data
        except Exception as e:
            logger.error(f"读取YAML文件失败: {file_path}, 错误: {str(e)}")
            raise

    @staticmethod
    def write_yaml(file_path: str, data: Union[Dict, List]):
        """
        写入YAML文件
        :param file_path: 文件路径
        :param data: 要写入的数据
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            logger.info(f"写入YAML文件成功: {file_path}")
        except Exception as e:
            logger.error(f"写入YAML文件失败: {file_path}, 错误: {str(e)}")
            raise

    @staticmethod
    def read_csv(file_path: str) -> List[Dict]:
        """
        读取CSV文件
        :param file_path: 文件路径
        :return: CSV数据列表
        """
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            logger.info(f"读取CSV文件成功: {file_path}")
            return data
        except Exception as e:
            logger.error(f"读取CSV文件失败: {file_path}, 错误: {str(e)}")
            raise

    @staticmethod
    def write_csv(file_path: str, data: List[Dict], fieldnames: List[str] = None):
        """
        写入CSV文件
        :param file_path: 文件路径
        :param data: 要写入的数据列表
        :param fieldnames: 字段名列表
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if not fieldnames and data:
                fieldnames = list(data[0].keys())

            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"写入CSV文件成功: {file_path}")
        except Exception as e:
            logger.error(f"写入CSV文件失败: {file_path}, 错误: {str(e)}")
            raise


class TestDataManager:
    """测试数据管理器"""

    @staticmethod
    def load_test_data(file_name: str) -> Union[Dict, List]:
        """
        从data/test_data目录加载测试数据
        :param file_name: 文件名（支持json和yaml）
        :return: 测试数据
        """
        file_path = os.path.join(Config.TEST_DATA_DIR, file_name)

        if file_name.endswith('.json'):
            return DataHandler.read_json(file_path)
        elif file_name.endswith(('.yaml', '.yml')):
            return DataHandler.read_yaml(file_path)
        elif file_name.endswith('.csv'):
            return DataHandler.read_csv(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_name}")

    @staticmethod
    def get_test_case_data(module: str, case_name: str) -> Dict:
        """
        获取指定测试用例的数据
        :param module: 模块名
        :param case_name: 用例名
        :return: 测试用例数据
        """
        file_name = f"{module}.json"
        all_data = TestDataManager.load_test_data(file_name)
        return all_data.get(case_name, {})
