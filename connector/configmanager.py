"""
配置管理模块，用于管理CTP连接器的配置信息
"""
import json
import os

class ConfigManager:
    """
    配置管理类，负责读取和管理配置信息
    """
    
    def __init__(self, config_file=None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认配置
        """
        self._config = {}
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
    
    def get_md_config(self):
        """
        获取行情服务配置
        
        Returns:
            dict: 行情服务配置字典
        """
        return self._config.get('md', {})
    
    def get_td_config(self):
        """
        获取交易服务配置
        
        Returns:
            dict: 交易服务配置字典
        """
        return self._config.get('td', {})
    
    def set_md_config(self, config):
        """
        设置行情服务配置
        
        Args:
            config: 行情服务配置字典
        """
        self._config['md'] = config
    
    def set_td_config(self, config):
        """
        设置交易服务配置
        
        Args:
            config: 交易服务配置字典
        """
        self._config['td'] = config
    
    def save_config(self, config_file):
        """
        保存配置到文件
        
        Args:
            config_file: 配置文件路径
        """
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=4)
