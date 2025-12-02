"""
数据库客户端工具类
支持MySQL、PostgreSQL等数据库操作
"""
from typing import List, Dict, Any, Optional
from utils.logger import logger


class MySQLClient:
    """MySQL数据库客户端"""

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """
        初始化MySQL客户端
        :param host: 数据库主机
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """连接数据库"""
        try:
            import pymysql
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            logger.info(f"MySQL数据库连接成功: {self.host}:{self.port}/{self.database}")
        except Exception as e:
            logger.error(f"MySQL数据库连接失败: {str(e)}")
            raise

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("MySQL数据库连接已关闭")

    def execute_query(self, sql: str, params: tuple = None) -> List[Dict]:
        """
        执行查询SQL
        :param sql: SQL语句
        :param params: 参数
        :return: 查询结果列表
        """
        try:
            logger.info(f"执行查询SQL: {sql}")
            if params:
                logger.info(f"参数: {params}")
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            logger.info(f"查询结果数量: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"SQL查询失败: {str(e)}")
            raise

    def execute_update(self, sql: str, params: tuple = None) -> int:
        """
        执行更新SQL（INSERT、UPDATE、DELETE）
        :param sql: SQL语句
        :param params: 参数
        :return: 影响的行数
        """
        try:
            logger.info(f"执行更新SQL: {sql}")
            if params:
                logger.info(f"参数: {params}")
            rows_affected = self.cursor.execute(sql, params)
            self.connection.commit()
            logger.info(f"影响行数: {rows_affected}")
            return rows_affected
        except Exception as e:
            self.connection.rollback()
            logger.error(f"SQL更新失败: {str(e)}")
            raise

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


class RedisClient:
    """Redis客户端"""

    def __init__(self, host: str, port: int, db: int = 0, password: str = None):
        """
        初始化Redis客户端
        :param host: Redis主机
        :param port: 端口
        :param db: 数据库编号
        :param password: 密码
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None

    def connect(self):
        """连接Redis"""
        try:
            import redis
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
            self.client.ping()
            logger.info(f"Redis连接成功: {self.host}:{self.port}/{self.db}")
        except Exception as e:
            logger.error(f"Redis连接失败: {str(e)}")
            raise

    def close(self):
        """关闭Redis连接"""
        if self.client:
            self.client.close()
        logger.info("Redis连接已关闭")

    def get(self, key: str) -> Optional[str]:
        """获取key的值"""
        return self.client.get(key)

    def set(self, key: str, value: str, ex: int = None):
        """
        设置key的值
        :param key: 键
        :param value: 值
        :param ex: 过期时间（秒）
        """
        self.client.set(key, value, ex=ex)

    def delete(self, *keys):
        """删除key"""
        self.client.delete(*keys)

    def exists(self, key: str) -> bool:
        """判断key是否存在"""
        return self.client.exists(key) > 0

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
