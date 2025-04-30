"""
CTP行情连接器实现
"""
import time
from openctp_ctp import mdapi
from .marketdataconnector import MarketDataConnector
from .constants import *
from .logger import get_default_log_file

class CTPMarketDataConnector(MarketDataConnector, mdapi.CThostFtdcMdSpi):
    """
    CTP行情连接器，实现行情服务连接、登录、订阅等功能
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls, *args, **kwargs):
        """
        获取单例实例
        
        Returns:
            CTPMarketDataConnector: 单例实例
        """
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    
    def __init__(self, front_address):
        """
        初始化CTP行情连接器
        
        Args:
            front_address: 前置地址
        """
        MarketDataConnector.__init__(self)
        mdapi.CThostFtdcMdSpi.__init__(self)
        
        self._front_address = front_address
        self._api = None
        self._connected = False
        self._logged_in = False
        self._user_id = ""
        self._password = ""
        self._subscribed_instruments = set()
        
        self.init_logger("CTPMarketDataConnector", "info")
    
    def connect(self):
        """
        连接到行情服务器
        """
        if self._api is not None:
            self.logger.info("Market data API already initialized, skipping connect")
            return
        
        self.status = CONNECTOR_STATUS_CONNECTING
        self.logger.info(f"Connecting to market data front: {self._front_address}")
        self._api = mdapi.CThostFtdcMdApi.CreateFtdcMdApi()
        self._api.RegisterFront(self._front_address)
        self._api.RegisterSpi(self)
        self._api.Init()
    
    def disconnect(self):
        """
        断开与行情服务器的连接
        """
        if self._api is not None:
            self.logger.info("Disconnecting from market data front")
            self._api.Release()
            self._api = None
        
        self._connected = False
        self._logged_in = False
        self.status = CONNECTOR_STATUS_DISCONNECTED
        self.logger.info("Disconnected from market data front")
    
    def is_connected(self):
        """
        检查是否已连接
        
        Returns:
            bool: 是否已连接
        """
        return self._connected
    
    def login(self, username="", password=""):
        """
        登录行情服务器
        
        Args:
            username: 用户名
            password: 密码
        """
        if not self._connected:
            self.logger.warning("Cannot login: not connected to market data front")
            return
        
        self._user_id = username
        self._password = password
        
        self.logger.info(f"Logging in to market data front with user: {username}")
        req = mdapi.CThostFtdcReqUserLoginField()
        req.UserID = username
        req.Password = password
        self._api.ReqUserLogin(req, 0)
    
    def subscribe(self, instruments):
        """
        订阅行情
        
        Args:
            instruments: 合约代码列表
        """
        if not self._logged_in or not instruments:
            self.logger.warning("Cannot subscribe: not logged in or empty instrument list")
            return
        
        self.logger.info(f"Subscribing to market data for instruments: {instruments}")
        encoded_instruments = [instrument.encode('utf-8') for instrument in instruments]
        self._api.SubscribeMarketData(encoded_instruments, len(instruments))
        
        for instrument in instruments:
            self._subscribed_instruments.add(instrument)
    
    def unsubscribe(self, instruments):
        """
        取消订阅行情
        
        Args:
            instruments: 合约代码列表
        """
        if not self._logged_in or not instruments:
            self.logger.warning("Cannot unsubscribe: not logged in or empty instrument list")
            return
        
        self.logger.info(f"Unsubscribing from market data for instruments: {instruments}")
        encoded_instruments = [instrument.encode('utf-8') for instrument in instruments]
        self._api.UnSubscribeMarketData(encoded_instruments, len(instruments))
        
        for instrument in instruments:
            if instrument in self._subscribed_instruments:
                self._subscribed_instruments.remove(instrument)
    
    def OnFrontConnected(self):
        """
        前置连接成功回调
        """
        self._connected = True
        self.status = CONNECTOR_STATUS_CONNECTED
        self.logger.info("Market data front connected")
        self.publish_event(EVENT_TYPE_CONNECTED)
        
        if self._user_id and self._password:
            self.logger.info("Auto login with saved credentials")
            self.login(self._user_id, self._password)
    
    def OnFrontDisconnected(self, reason):
        """
        前置断开连接回调
        
        Args:
            reason: 断开原因
        """
        self._connected = False
        self._logged_in = False
        self.status = CONNECTOR_STATUS_DISCONNECTED
        self.logger.warning(f"Market data front disconnected, reason: {reason}")
        self.publish_event(EVENT_TYPE_DISCONNECTED, {"reason": reason})
    
    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, requestID, isLast):
        """
        用户登录回调
        
        Args:
            pRspUserLogin: 登录回调信息
            pRspInfo: 响应信息
            requestID: 请求ID
            isLast: 是否最后一个响应
        """
        if pRspInfo is not None and pRspInfo.ErrorID != 0:
            error_msg = f"Market data login failed: {pRspInfo.ErrorMsg}, ErrorID: {pRspInfo.ErrorID}"
            self.logger.error(error_msg)
            self.publish_event(EVENT_TYPE_LOGIN_FAILED, {
                "error_id": pRspInfo.ErrorID,
                "error_msg": pRspInfo.ErrorMsg
            })
            return
        
        self._logged_in = True
        self.status = CONNECTOR_STATUS_READY
        
        login_info = {
            "trading_day": pRspUserLogin.TradingDay,
            "login_time": pRspUserLogin.LoginTime,
            "system_name": pRspUserLogin.SystemName
        }
        
        self.logger.info(f"Market data login successful. Trading day: {pRspUserLogin.TradingDay}")
        self.publish_event(EVENT_TYPE_LOGIN_SUCCESS, login_info)
        
        if self._subscribed_instruments:
            self.logger.info(f"Re-subscribing to {len(self._subscribed_instruments)} instruments")
            self.subscribe(list(self._subscribed_instruments))
    
    def OnRtnDepthMarketData(self, pDepthMarketData):
        """
        深度行情通知
        
        Args:
            pDepthMarketData: 深度行情数据
        """
        market_data = {
            "instrument_id": pDepthMarketData.InstrumentID,
            "exchange_id": pDepthMarketData.ExchangeID,
            "last_price": pDepthMarketData.LastPrice,
            "volume": pDepthMarketData.Volume,
            "turnover": pDepthMarketData.Turnover,
            "open_interest": pDepthMarketData.OpenInterest,
            "open_price": pDepthMarketData.OpenPrice,
            "highest_price": pDepthMarketData.HighestPrice,
            "lowest_price": pDepthMarketData.LowestPrice,
            "upper_limit_price": pDepthMarketData.UpperLimitPrice,
            "lower_limit_price": pDepthMarketData.LowerLimitPrice,
            "bid_price1": pDepthMarketData.BidPrice1,
            "bid_volume1": pDepthMarketData.BidVolume1,
            "ask_price1": pDepthMarketData.AskPrice1,
            "ask_volume1": pDepthMarketData.AskVolume1,
            "update_time": pDepthMarketData.UpdateTime,
            "update_millisec": pDepthMarketData.UpdateMillisec,
            "trading_day": pDepthMarketData.TradingDay
        }
        
        if self.logger and self.logger.isEnabledFor(10):  # DEBUG level
            self.logger.debug(f"Market data received: {pDepthMarketData.InstrumentID}, price: {pDepthMarketData.LastPrice}")
        
        self.publish_event(EVENT_TYPE_MARKET_DATA, market_data)
    
    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, requestID, isLast):
        """
        订阅行情回调
        
        Args:
            pSpecificInstrument: 合约信息
            pRspInfo: 响应信息
            requestID: 请求ID
            isLast: 是否最后一个响应
        """
        if pRspInfo is not None and pRspInfo.ErrorID != 0:
            self.logger.error(f"Subscribe failed. [{pSpecificInstrument.InstrumentID}] {pRspInfo.ErrorMsg}")
            return
        
        self.logger.info(f"Subscribe succeed. {pSpecificInstrument.InstrumentID}")
