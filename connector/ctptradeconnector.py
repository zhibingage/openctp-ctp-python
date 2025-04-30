"""
CTP交易连接器实现
"""
import time
from openctp_ctp import tdapi
from .tradeconnector import TradeConnector
from .constants import *
from .logger import get_default_log_file

class CTPTradeConnector(TradeConnector, tdapi.CThostFtdcTraderSpi):
    """
    CTP交易连接器，实现交易服务连接、登录、身份验证、结算单确认等功能
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls, *args, **kwargs):
        """
        获取单例实例
        
        Returns:
            CTPTradeConnector: 单例实例
        """
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    
    def __init__(self, front_address):
        """
        初始化CTP交易连接器
        
        Args:
            front_address: 前置地址
        """
        TradeConnector.__init__(self)
        tdapi.CThostFtdcTraderSpi.__init__(self)
        
        self._front_address = front_address
        self._api = None
        self._connected = False
        self._authenticated = False
        self._logged_in = False
        self._settlement_confirmed = False
        
        self._broker_id = ""
        self._user_id = ""
        self._password = ""
        self._app_id = ""
        self._auth_code = ""
        
        self._trading_day = ""
        self._front_id = 0
        self._session_id = 0
        self._order_ref = 0
        
        self.init_logger("CTPTradeConnector", "info")
    
    def connect(self):
        """
        连接到交易服务器
        """
        if self._api is not None:
            self.logger.info("Trade API already initialized, skipping connect")
            return
        
        self.status = CONNECTOR_STATUS_CONNECTING
        self.logger.info(f"Connecting to trade front: {self._front_address}")
        self._api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi()
        self._api.RegisterSpi(self)
        self._api.RegisterFront(self._front_address)
        self._api.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
        self._api.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
        self._api.Init()
    
    def disconnect(self):
        """
        断开与交易服务器的连接
        """
        if self._api is not None:
            self.logger.info("Disconnecting from trade front")
            self._api.Release()
            self._api = None
        
        self._connected = False
        self._authenticated = False
        self._logged_in = False
        self._settlement_confirmed = False
        self.status = CONNECTOR_STATUS_DISCONNECTED
        self.logger.info("Disconnected from trade front")
    
    def is_connected(self):
        """
        检查是否已连接
        
        Returns:
            bool: 是否已连接
        """
        return self._connected
    
    def authenticate(self, broker_id, user_id, app_id, auth_code):
        """
        客户端认证
        
        Args:
            broker_id: 经纪商代码
            user_id: 用户代码
            app_id: App代码
            auth_code: 认证码
        """
        if not self._connected or self._api is None:
            self.logger.warning("Cannot authenticate: not connected to trade front or API is None")
            return
        
        self._broker_id = broker_id
        self._user_id = user_id
        self._app_id = app_id
        self._auth_code = auth_code
        
        self.logger.info(f"Authenticating with broker: {broker_id}, user: {user_id}, app: {app_id}")
        req = tdapi.CThostFtdcReqAuthenticateField()
        req.BrokerID = broker_id
        req.UserID = user_id
        req.AppID = app_id
        req.AuthCode = auth_code
        self._api.ReqAuthenticate(req, 0)
    
    def login(self, broker_id, user_id, password):
        """
        登录交易服务器
        
        Args:
            broker_id: 经纪商代码
            user_id: 用户代码
            password: 密码
        """
        if not self._connected or self._api is None:
            self.logger.warning("Cannot login: not connected to trade front or API is None")
            return
        
        if not self._authenticated and self._app_id and self._auth_code:
            self.logger.info(f"Authentication required before login, authenticating with broker: {broker_id}, user: {user_id}")
            self.authenticate(broker_id, user_id, self._app_id, self._auth_code)
            return
        
        self._broker_id = broker_id
        self._user_id = user_id
        self._password = password
        
        self.logger.info(f"Logging in to trade front with broker: {broker_id}, user: {user_id}")
        req = tdapi.CThostFtdcReqUserLoginField()
        req.BrokerID = broker_id
        req.UserID = user_id
        req.Password = password
        req.UserProductInfo = "openctp_ctp_python"
        self._api.ReqUserLogin(req, 0)
    
    def confirm_settlement(self):
        """
        确认结算单
        """
        if not self._logged_in or self._api is None:
            self.logger.warning("Cannot confirm settlement: not logged in or API is None")
            return
        
        self.logger.info(f"Confirming settlement for broker: {self._broker_id}, investor: {self._user_id}")
        req = tdapi.CThostFtdcSettlementInfoConfirmField()
        req.BrokerID = self._broker_id
        req.InvestorID = self._user_id
        self._api.ReqSettlementInfoConfirm(req, 0)
    
    def query_instruments(self, exchange_id="", product_id="", instrument_id=""):
        """
        查询合约
        
        Args:
            exchange_id: 交易所代码
            product_id: 产品代码
            instrument_id: 合约代码
        """
        if not self._logged_in or self._api is None:
            self.logger.warning("Cannot query instruments: not logged in or API is None")
            return
        
        self.logger.info(f"Querying instruments - exchange: {exchange_id}, product: {product_id}, instrument: {instrument_id}")
        req = tdapi.CThostFtdcQryInstrumentField()
        req.ExchangeID = exchange_id
        req.ProductID = product_id
        req.InstrumentID = instrument_id
        self._api.ReqQryInstrument(req, 0)
    
    def query_trading_account(self):
        """
        查询资金账户
        """
        if not self._logged_in or self._api is None:
            self.logger.warning("Cannot query trading account: not logged in or API is None")
            return
        
        self.logger.info(f"Querying trading account for broker: {self._broker_id}, investor: {self._user_id}")
        req = tdapi.CThostFtdcQryTradingAccountField()
        req.BrokerID = self._broker_id
        req.InvestorID = self._user_id
        self._api.ReqQryTradingAccount(req, 0)
    
    def query_positions(self, instrument_id=""):
        """
        查询持仓
        
        Args:
            instrument_id: 合约代码
        """
        if not self._logged_in or self._api is None:
            self.logger.warning("Cannot query positions: not logged in or API is None")
            return
        
        self.logger.info(f"Querying positions for broker: {self._broker_id}, investor: {self._user_id}, instrument: {instrument_id or 'all'}")
        req = tdapi.CThostFtdcQryInvestorPositionField()
        req.BrokerID = self._broker_id
        req.InvestorID = self._user_id
        req.InstrumentID = instrument_id
        self._api.ReqQryInvestorPosition(req, 0)
    
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
        if not self._logged_in or not self._settlement_confirmed or self._api is None:
            self.logger.warning("Cannot insert order: not logged in, settlement not confirmed, or API is None")
            return
        
        self._order_ref += 1
        
        direction_str = "Buy" if direction == tdapi.THOST_FTDC_D_Buy else "Sell"
        offset_str = "Open" if offset == tdapi.THOST_FTDC_OF_Open else "Close"
        
        self.logger.info(f"Inserting order - instrument: {instrument_id}, exchange: {exchange_id}, "
                         f"direction: {direction_str}, offset: {offset_str}, price: {price}, volume: {volume}, "
                         f"order_ref: {self._order_ref}")
        
        req = tdapi.CThostFtdcInputOrderField()
        req.BrokerID = self._broker_id
        req.UserID = self._user_id
        req.InvestorID = self._user_id
        req.ExchangeID = exchange_id
        req.InstrumentID = instrument_id
        req.Direction = direction
        req.CombOffsetFlag = offset
        req.CombHedgeFlag = tdapi.THOST_FTDC_HF_Speculation
        req.OrderPriceType = tdapi.THOST_FTDC_OPT_LimitPrice
        req.LimitPrice = float(price)
        req.VolumeTotalOriginal = int(volume)
        req.TimeCondition = tdapi.THOST_FTDC_TC_GFD
        req.VolumeCondition = tdapi.THOST_FTDC_VC_AV
        req.MinVolume = 1
        req.OrderRef = str(self._order_ref)
        req.ForceCloseReason = tdapi.THOST_FTDC_FCC_NotForceClose
        req.ContingentCondition = tdapi.THOST_FTDC_CC_Immediately
        
        self._api.ReqOrderInsert(req, 0)
        
        return self._order_ref
    
    def order_cancel(self, order_ref, exchange_id, instrument_id, order_sys_id=""):
        """
        撤单
        
        Args:
            order_ref: 报单引用
            exchange_id: 交易所代码
            instrument_id: 合约代码
            order_sys_id: 报单编号
        """
        if not self._logged_in or not self._settlement_confirmed or self._api is None:
            self.logger.warning("Cannot cancel order: not logged in, settlement not confirmed, or API is None")
            return
        
        self.logger.info(f"Cancelling order - order_ref: {order_ref}, exchange: {exchange_id}, "
                         f"instrument: {instrument_id}, order_sys_id: {order_sys_id or 'N/A'}")
        
        req = tdapi.CThostFtdcInputOrderActionField()
        req.BrokerID = self._broker_id
        req.UserID = self._user_id
        req.InvestorID = self._user_id
        req.ExchangeID = exchange_id
        req.InstrumentID = instrument_id
        req.OrderSysID = order_sys_id
        req.FrontID = self._front_id
        req.SessionID = self._session_id
        req.OrderRef = order_ref
        req.ActionFlag = tdapi.THOST_FTDC_AF_Delete
        
        self._api.ReqOrderAction(req, 0)
    
    def OnFrontConnected(self):
        """
        前置连接成功回调
        """
        self._connected = True
        self.status = CONNECTOR_STATUS_CONNECTED
        self.logger.info(f"Trade front connected to {self._front_address}")
        self.publish_event(EVENT_TYPE_CONNECTED)
        
        if self._broker_id and self._user_id and self._app_id and self._auth_code:
            self.logger.info("Auto authenticating with saved credentials")
            self.authenticate(self._broker_id, self._user_id, self._app_id, self._auth_code)
        elif self._broker_id and self._user_id and self._password:
            self.logger.info("Auto logging in with saved credentials")
            self.login(self._broker_id, self._user_id, self._password)
    
    def OnFrontDisconnected(self, reason):
        """
        前置断开连接回调
        
        Args:
            reason: 断开原因
        """
        self._connected = False
        self._authenticated = False
        self._logged_in = False
        self._settlement_confirmed = False
        self.status = CONNECTOR_STATUS_DISCONNECTED
        self.logger.warning(f"Trade front disconnected, reason: {reason}")
        self.publish_event(EVENT_TYPE_DISCONNECTED, {"reason": reason})
    
    def OnRspAuthenticate(self, pRspAuthenticateField, pRspInfo, requestID, isLast):
        """
        客户端认证回调
        
        Args:
            pRspAuthenticateField: 认证回调信息
            pRspInfo: 响应信息
            requestID: 请求ID
            isLast: 是否最后一个响应
        """
        if pRspInfo is not None and pRspInfo.ErrorID != 0:
            error_msg = f"Authentication failed: {pRspInfo.ErrorMsg}, ErrorID: {pRspInfo.ErrorID}"
            self.logger.error(error_msg)
            self.publish_event(EVENT_TYPE_AUTH_FAILED, {
                "error_id": pRspInfo.ErrorID,
                "error_msg": pRspInfo.ErrorMsg
            })
            return
        
        self._authenticated = True
        self.logger.info("Authentication successful")
        self.publish_event(EVENT_TYPE_AUTH_SUCCESS)
        
        if self._broker_id and self._user_id and self._password:
            self.logger.info("Auto logging in after successful authentication")
            self.login(self._broker_id, self._user_id, self._password)
    
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
            error_msg = f"Login failed: {pRspInfo.ErrorMsg}, ErrorID: {pRspInfo.ErrorID}"
            self.logger.error(error_msg)
            self.publish_event(EVENT_TYPE_LOGIN_FAILED, {
                "error_id": pRspInfo.ErrorID,
                "error_msg": pRspInfo.ErrorMsg
            })
            return
        
        self._logged_in = True
        self.status = CONNECTOR_STATUS_LOGGED_IN
        
        self._trading_day = pRspUserLogin.TradingDay
        self._front_id = pRspUserLogin.FrontID
        self._session_id = pRspUserLogin.SessionID
        self._order_ref = int(pRspUserLogin.MaxOrderRef) if pRspUserLogin.MaxOrderRef else 0
        
        login_info = {
            "trading_day": pRspUserLogin.TradingDay,
            "login_time": pRspUserLogin.LoginTime,
            "system_name": pRspUserLogin.SystemName,
            "front_id": pRspUserLogin.FrontID,
            "session_id": pRspUserLogin.SessionID,
            "max_order_ref": pRspUserLogin.MaxOrderRef
        }
        
        self.logger.info(f"Login successful. Trading day: {pRspUserLogin.TradingDay}, "
                         f"Front ID: {pRspUserLogin.FrontID}, Session ID: {pRspUserLogin.SessionID}")
        self.publish_event(EVENT_TYPE_LOGIN_SUCCESS, login_info)
        
        self.logger.info("Auto confirming settlement after successful login")
        self.confirm_settlement()
    
    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, requestID, isLast):
        """
        结算单确认回调
        
        Args:
            pSettlementInfoConfirm: 结算单确认回调信息
            pRspInfo: 响应信息
            requestID: 请求ID
            isLast: 是否最后一个响应
        """
        if pRspInfo is not None and pRspInfo.ErrorID != 0:
            self.logger.error(f"Settlement confirm failed: {pRspInfo.ErrorMsg}, ErrorID: {pRspInfo.ErrorID}")
            return
        
        self._settlement_confirmed = True
        self.status = CONNECTOR_STATUS_READY
        
        settlement_info = {
            "broker_id": pSettlementInfoConfirm.BrokerID,
            "investor_id": pSettlementInfoConfirm.InvestorID,
            "confirm_date": pSettlementInfoConfirm.ConfirmDate,
            "confirm_time": pSettlementInfoConfirm.ConfirmTime
        }
        
        self.logger.info(f"Settlement confirmed. Date: {pSettlementInfoConfirm.ConfirmDate}, Time: {pSettlementInfoConfirm.ConfirmTime}")
        self.publish_event(EVENT_TYPE_SETTLEMENT_CONFIRMED, settlement_info)
    
    def OnRtnOrder(self, pOrder):
        """
        报单通知
        
        Args:
            pOrder: 报单信息
        """
        order_info = {
            "broker_id": pOrder.BrokerID,
            "investor_id": pOrder.InvestorID,
            "instrument_id": pOrder.InstrumentID,
            "order_ref": pOrder.OrderRef,
            "user_id": pOrder.UserID,
            "order_price_type": pOrder.OrderPriceType,
            "direction": pOrder.Direction,
            "combo_offset_flag": pOrder.CombOffsetFlag,
            "combo_hedge_flag": pOrder.CombHedgeFlag,
            "limit_price": pOrder.LimitPrice,
            "volume_total_original": pOrder.VolumeTotalOriginal,
            "time_condition": pOrder.TimeCondition,
            "volume_condition": pOrder.VolumeCondition,
            "min_volume": pOrder.MinVolume,
            "contingent_condition": pOrder.ContingentCondition,
            "stop_price": pOrder.StopPrice,
            "force_close_reason": pOrder.ForceCloseReason,
            "order_local_id": pOrder.OrderLocalID,
            "exchange_id": pOrder.ExchangeID,
            "participant_id": pOrder.ParticipantID,
            "client_id": pOrder.ClientID,
            "exchange_inst_id": pOrder.ExchangeInstID,
            "trader_id": pOrder.TraderID,
            "install_id": pOrder.InstallID,
            "order_submit_status": pOrder.OrderSubmitStatus,
            "notify_sequence": pOrder.NotifySequence,
            "trading_day": pOrder.TradingDay,
            "settlement_id": pOrder.SettlementID,
            "order_sys_id": pOrder.OrderSysID,
            "order_source": pOrder.OrderSource,
            "order_status": pOrder.OrderStatus,
            "order_type": pOrder.OrderType,
            "volume_traded": pOrder.VolumeTraded,
            "volume_total": pOrder.VolumeTotal,
            "insert_date": pOrder.InsertDate,
            "insert_time": pOrder.InsertTime,
            "active_time": pOrder.ActiveTime,
            "suspend_time": pOrder.SuspendTime,
            "update_time": pOrder.UpdateTime,
            "cancel_time": pOrder.CancelTime,
            "active_trader_id": pOrder.ActiveTraderID,
            "clearing_part_id": pOrder.ClearingPartID,
            "sequence_no": pOrder.SequenceNo,
            "front_id": pOrder.FrontID,
            "session_id": pOrder.SessionID,
            "user_product_info": pOrder.UserProductInfo,
            "status_msg": pOrder.StatusMsg,
            "user_force_close": pOrder.UserForceClose,
            "active_user_id": pOrder.ActiveUserID,
            "broker_order_seq": pOrder.BrokerOrderSeq,
            "relative_order_sys_id": pOrder.RelativeOrderSysID,
            "zce_total_traded_volume": pOrder.ZCETotalTradedVolume,
            "is_swap_order": pOrder.IsSwapOrder,
            "branch_id": pOrder.BranchID,
            "investment_unit_id": pOrder.InvestUnitID,
            "currency_id": pOrder.CurrencyID,
            "ip_address": pOrder.IPAddress,
            "mac_address": pOrder.MacAddress
        }
        
        direction_str = "Buy" if pOrder.Direction == tdapi.THOST_FTDC_D_Buy else "Sell"
        status_map = {
            tdapi.THOST_FTDC_OST_AllTraded: "All Traded",
            tdapi.THOST_FTDC_OST_PartTradedQueueing: "Partially Traded",
            tdapi.THOST_FTDC_OST_NoTradeQueueing: "In Queue",
            tdapi.THOST_FTDC_OST_Canceled: "Canceled",
            tdapi.THOST_FTDC_OST_Unknown: "Unknown"
        }
        status_str = status_map.get(pOrder.OrderStatus, f"Status Code: {pOrder.OrderStatus}")
        
        self.logger.info(f"Order update - instrument: {pOrder.InstrumentID}, direction: {direction_str}, "
                         f"price: {pOrder.LimitPrice}, status: {status_str}, "
                         f"traded/total: {pOrder.VolumeTraded}/{pOrder.VolumeTotalOriginal}, "
                         f"order_ref: {pOrder.OrderRef}, order_sys_id: {pOrder.OrderSysID}")
        
        self.publish_event(EVENT_TYPE_ORDER_STATUS, order_info)
    
    def OnRtnTrade(self, pTrade):
        """
        成交通知
        
        Args:
            pTrade: 成交信息
        """
        trade_info = {
            "broker_id": pTrade.BrokerID,
            "investor_id": pTrade.InvestorID,
            "instrument_id": pTrade.InstrumentID,
            "order_ref": pTrade.OrderRef,
            "user_id": pTrade.UserID,
            "exchange_id": pTrade.ExchangeID,
            "trade_id": pTrade.TradeID,
            "direction": pTrade.Direction,
            "order_sys_id": pTrade.OrderSysID,
            "participant_id": pTrade.ParticipantID,
            "client_id": pTrade.ClientID,
            "trading_role": pTrade.TradingRole,
            "exchange_inst_id": pTrade.ExchangeInstID,
            "offset_flag": pTrade.OffsetFlag,
            "hedge_flag": pTrade.HedgeFlag,
            "price": pTrade.Price,
            "volume": pTrade.Volume,
            "trade_date": pTrade.TradeDate,
            "trade_time": pTrade.TradeTime,
            "trade_type": pTrade.TradeType,
            "price_source": pTrade.PriceSource,
            "trader_id": pTrade.TraderID,
            "order_local_id": pTrade.OrderLocalID,
            "clearing_part_id": pTrade.ClearingPartID,
            "business_unit": pTrade.BusinessUnit,
            "sequence_no": pTrade.SequenceNo,
            "trading_day": pTrade.TradingDay,
            "settlement_id": pTrade.SettlementID,
            "broker_order_seq": pTrade.BrokerOrderSeq,
            "trade_source": pTrade.TradeSource,
            "investment_unit_id": pTrade.InvestUnitID,
            "currency_id": pTrade.CurrencyID
        }
        
        direction_str = "Buy" if pTrade.Direction == tdapi.THOST_FTDC_D_Buy else "Sell"
        offset_map = {
            tdapi.THOST_FTDC_OF_Open: "Open",
            tdapi.THOST_FTDC_OF_Close: "Close",
            tdapi.THOST_FTDC_OF_CloseToday: "Close Today",
            tdapi.THOST_FTDC_OF_CloseYesterday: "Close Yesterday",
            tdapi.THOST_FTDC_OF_ForceClose: "Force Close"
        }
        offset_str = offset_map.get(pTrade.OffsetFlag, f"Offset Code: {pTrade.OffsetFlag}")
        
        self.logger.info(f"Trade executed - instrument: {pTrade.InstrumentID}, direction: {direction_str}, "
                         f"offset: {offset_str}, price: {pTrade.Price}, volume: {pTrade.Volume}, "
                         f"trade_id: {pTrade.TradeID}, order_sys_id: {pTrade.OrderSysID}, "
                         f"trade_time: {pTrade.TradeTime}")
        
        self.publish_event(EVENT_TYPE_TRADE, trade_info)
