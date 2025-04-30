"""
行情连接器基类定义
"""
from abc import abstractmethod
from .baseconnector import BaseConnector

class MarketDataConnector(BaseConnector):
    """
    行情连接器基类，定义行情连接器通用接口
    """
    
    def __init__(self):
        """
        初始化行情连接器
        """
        super().__init__()
    
    @abstractmethod
    def login(self, username="", password=""):
        """
        登录行情服务器
        
        Args:
            username: 用户名
            password: 密码
        """
        pass
    
    @abstractmethod
    def subscribe(self, instruments):
        """
        订阅行情
        
        Args:
            instruments: 合约代码列表
        """
        pass
    
    @abstractmethod
    def unsubscribe(self, instruments):
        """
        取消订阅行情
        
        Args:
            instruments: 合约代码列表
        """
        pass
