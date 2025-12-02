"""
配置管理器
负责加载、保存和管理配置
"""
import yaml
from pathlib import Path
from typing import Any, Optional, Dict
from loguru import logger


class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "default_config.yaml"
    USER_CONFIG_PATH = Path(__file__).parent.parent / "config" / "user_config.yaml"

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 自定义配置文件路径
        """
        self.config_path = Path(config_path) if config_path else self.USER_CONFIG_PATH
        self.config: Dict = {}
        self.load()

    def load(self):
        """加载配置"""
        try:
            # 加载默认配置
            with open(self.DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
                default_config = yaml.safe_load(f)

            # 如果用户配置存在，合并配置
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                # 深度合并
                self.config = self._deep_merge(default_config, user_config)
                logger.info(f"配置已加载: {self.config_path}")
            else:
                self.config = default_config
                logger.info("使用默认配置")

        except Exception as e:
            logger.error(f"配置加载失败: {e}")
            self.config = {}

    def save(self, path: Optional[str] = None):
        """
        保存配置

        Args:
            path: 保存路径（None则保存到用户配置）
        """
        try:
            save_path = Path(path) if path else self.config_path
            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.config, f, allow_unicode=True, default_flow_style=False)

            logger.success(f"配置已保存: {save_path}")

        except Exception as e:
            logger.error(f"配置保存失败: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值（支持点号分隔的嵌套键）

        Args:
            key: 配置键，支持 "tts.edge.default_voice" 格式
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config

        # 导航到最后一层
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # 设置值
        config[keys[-1]] = value
        logger.debug(f"配置已更新: {key} = {value}")

    def get_tts_config(self) -> Dict:
        """获取TTS配置"""
        return self.get('tts', {})

    def get_audio_config(self) -> Dict:
        """获取音频配置"""
        return self.get('audio', {})

    def get_text_config(self) -> Dict:
        """获取文本处理配置"""
        return self.get('text', {})

    def get_output_config(self) -> Dict:
        """获取输出配置"""
        return self.get('output', {})

    def reset_to_default(self):
        """重置为默认配置"""
        with open(self.DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        logger.info("配置已重置为默认值")

    @staticmethod
    def _deep_merge(base: dict, override: dict) -> dict:
        """
        深度合并字典

        Args:
            base: 基础字典
            override: 覆盖字典

        Returns:
            合并后的字典
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigManager._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def export_template(self, output_path: str):
        """
        导出配置模板

        Args:
            output_path: 输出路径
        """
        self.save(output_path)
        logger.info(f"配置模板已导出: {output_path}")

    def __str__(self) -> str:
        """字符串表示"""
        return yaml.dump(self.config, allow_unicode=True, default_flow_style=False)


if __name__ == '__main__':
    # 测试代码
    config = ConfigManager()

    # 获取配置
    print("默认引擎:", config.get('tts.default_engine'))
    print("默认音色:", config.get('tts.edge.default_voice'))
    print("输出格式:", config.get('audio.output_format'))

    # 设置配置
    config.set('tts.edge.speech_rate', 1.2)
    print("语速:", config.get('tts.edge.speech_rate'))

    # 保存配置
    # config.save()
