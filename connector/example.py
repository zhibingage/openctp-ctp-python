"""
连接器使用示例
"""
import time
from openctp_ctp import tdapi
from .constants import *
from .configmanager import ConfigManager
from .connectorfactory import ConnectorFactory

def on_market_data(event_type, data):
    """
    行情数据回调
    
    Args:
        event_type: 事件类型
        data: 事件数据
    """
    print(f"Market data: {data['instrument_id']} - {data['last_price']}")

def on_order_status(event_type, data):
    """
    订单状态回调
    
    Args:
        event_type: 事件类型
        data: 事件数据
    """
    print(f"Order status: {data['instrument_id']} - {data['order_status']}")

def on_trade(event_type, data):
    """
    成交回调
    
    Args:
        event_type: 事件类型
        data: 事件数据
    """
    print(f"Trade: {data['instrument_id']} - {data['price']} - {data['volume']}")

def main():
    """
    主函数
    """
    config_manager = ConfigManager()
    
    md_config = {
        "front_address": "tcp://180.168.146.187:10131",
        "user_id": "",
        "password": ""
    }
    config_manager.set_md_config(md_config)
    
    td_config = {
        "front_address": "tcp://180.168.146.187:10130",
        "broker_id": "9999",
        "user_id": "000001",
        "password": "888888",
        "app_id": "simnow_client_test",
        "auth_code": "0000000000000000"
    }
    config_manager.set_td_config(td_config)
    
    md_connector = ConnectorFactory.create_market_data_connector(
        'ctp', md_config['front_address']
    )
    
    td_connector = ConnectorFactory.create_trade_connector(
        'ctp', td_config['front_address']
    )
    
    md_connector.subscribe_event(EVENT_TYPE_MARKET_DATA, on_market_data)
    td_connector.subscribe_event(EVENT_TYPE_ORDER_STATUS, on_order_status)
    td_connector.subscribe_event(EVENT_TYPE_TRADE, on_trade)
    
    md_connector.connect()
    
    td_connector.connect()
    
    td_connector.authenticate(
        td_config['broker_id'],
        td_config['user_id'],
        td_config['app_id'],
        td_config['auth_code']
    )
    
    time.sleep(5)
    
    md_connector.subscribe(['au2406'])
    
    td_connector.query_positions()
    
    td_connector.query_trading_account()
    
    order_ref = td_connector.order_insert(
        instrument_id='au2406',
        exchange_id='SHFE',
        price=400.0,
        volume=1,
        direction=tdapi.THOST_FTDC_D_Buy,
        offset=tdapi.THOST_FTDC_OF_Open
    )
    
    time.sleep(5)
    
    td_connector.order_cancel(
        order_ref=str(order_ref),
        exchange_id='SHFE',
        instrument_id='au2406'
    )
    
    time.sleep(5)
    
    md_connector.disconnect()
    td_connector.disconnect()

if __name__ == '__main__':
    main()
