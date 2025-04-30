"""
交易连接器基类定义
"""
from abc import abstractmethod
from .baseconnector import BaseConnector

class TradeConnector(BaseConnector):
    """
    交易连接器基类，定义交易连接器通用接口
    """
    
    def __init__(self):
        """
        初始化交易连接器
        """
        super().__init__()
    
    @abstractmethod
    def authenticate(self, broker_id, user_id, app_id, auth_code):
        """
        客户端认证
        
        Args:
            broker_id: 经纪商代码
            user_id: 用户代码
            app_id: App代码
            auth_code: 认证码
        """
        pass
    
    @abstractmethod
    def login(self, broker_id, user_id, password):
        """
        登录交易服务器
        
        Args:
            broker_id: 经纪商代码
            user_id: 用户代码
            password: 密码
        """
        pass
    
    @abstractmethod
    def confirm_settlement(self):
        """
        确认结算单
        """
        pass
    
    @abstractmethod
    def query_instruments(self, exchange_id="", product_id="", instrument_id=""):
        """
        查询合约
        
        Args:
            exchange_id: 交易所代码
            product_id: 产品代码
            instrument_id: 合约代码
        """
        pass
    
    @abstractmethod
    def query_trading_account(self):
        """
        查询资金账户
        """
        pass
    
    @abstractmethod
    def query_positions(self, instrument_id=""):
        """
        查询持仓
        
        Args:
            instrument_id: 合约代码
        """
        pass
    
    @abstractmethod
    def order_insert(self, instrument_id, exchange_id, price, volume, direction, offset):
        """
        报单
        
        Args:
            instrument_id: 合约代码
            exchange_id: 交易所代码
            price: 价格
            volume: 数量
            direction: 买卖方向
            offset: 开平标志
        """
        pass
    
    @abstractmethod
    def order_cancel(self, order_ref, exchange_id, instrument_id, order_sys_id=""):
        """
        撤单
        
        Args:
            order_ref: 报单引用
            exchange_id: 交易所代码
            instrument_id: 合约代码
            order_sys_id: 报单编号
        """
        pass
