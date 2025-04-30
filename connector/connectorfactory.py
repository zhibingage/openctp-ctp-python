"""
连接器工厂，用于创建不同类型的连接器实例
"""
from .ctpmarketdataconnector import CTPMarketDataConnector
from .ctptradeconnector import CTPTradeConnector

class ConnectorFactory:
    """
    连接器工厂类，负责创建不同类型的连接器实例
    """
    
    @staticmethod
    def create_market_data_connector(connector_type, *args, **kwargs):
        """
        创建行情连接器
        
        Args:
            connector_type: 连接器类型，如 'ctp'
            args: 位置参数
            kwargs: 关键字参数
        
        Returns:
            MarketDataConnector: 行情连接器实例
        """
        if connector_type.lower() == 'ctp':
            return CTPMarketDataConnector.get_instance(*args, **kwargs)
        else:
            raise ValueError(f"Unsupported market data connector type: {connector_type}")
    
    @staticmethod
    def create_trade_connector(connector_type, *args, **kwargs):
        """
        创建交易连接器
        
        Args:
            connector_type: 连接器类型，如 'ctp'
            args: 位置参数
            kwargs: 关键字参数
        
        Returns:
            TradeConnector: 交易连接器实例
        """
        if connector_type.lower() == 'ctp':
            return CTPTradeConnector.get_instance(*args, **kwargs)
        else:
            raise ValueError(f"Unsupported trade connector type: {connector_type}")
