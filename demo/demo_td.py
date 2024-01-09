"""
    手动下载配置时的交易测试文件
"""
import sys
import time
import os

import thosttraderapi as tdapi

# 前置地址 参考 http://121.37.80.177:50080/detail.html  SimNow
FrontAddr = ""

# 登录信息 需要在 SimNow https://www.simnow.com.cn/ 平台注册账号
userid = ""
password = ""
brokerid = "9999"
authcode = "0000000000000000"
appid = "simnow_client_test"


class CTdSpiImpl(tdapi.CThostFtdcTraderSpi):
    """交易回调实现类"""

    def __init__(self):
        super().__init__()

        flow_path = os.path.join(os.getcwd(), "flow_logs", userid)
        if not os.path.exists(flow_path):
            os.makedirs(flow_path)
        flow_path = os.path.join(flow_path, userid)
        self._api: tdapi.CThostFtdcTraderApi = (
            tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(flow_path)
        )

        print("CTP交易API版本号:", self._api.GetApiVersion())

        # 注册交易前置
        self._api.RegisterFront(FrontAddr)
        # 注册交易回调实例
        self._api.RegisterSpi(self)
        # 订阅私有流
        self._api.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
        # 订阅公有流
        self._api.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
        # 初始化交易实例
        self._api.Init()

    def OnFrontConnected(self):
        """交易前置连接成功"""
        print("交易前置连接成功")
        self.authenticate()

    def OnFrontDisconnected(self, nReason: int):
        """交易前置连接断开"""
        print("交易前置连接断开: nReason=", nReason)

    def authenticate(self):
        """认证 demo"""
        print("> 认证请求")
        _req = tdapi.CThostFtdcReqAuthenticateField()
        _req.BrokerID = brokerid
        _req.UserID = userid
        _req.AppID = appid
        _req.AuthCode = authcode
        self._api.ReqAuthenticate(_req, 0)

    def OnRspAuthenticate(
            self,
            pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
            pRspInfo: tdapi.CThostFtdcRspInfoField,
            nRequestID: int,
            bIsLast: bool,
    ):
        """客户端认证响应"""
        if pRspInfo:
            print("认证响应", pRspInfo.ErrorID, pRspInfo.ErrorMsg)
        if pRspInfo and pRspInfo.ErrorID != 0:
            return

        # 登录
        self.login()

    def login(self):
        """登录 demo"""
        print("> 登录请求")

        _req = tdapi.CThostFtdcReqUserLoginField()
        _req.BrokerID = brokerid
        _req.UserID = userid
        _req.Password = password
        if sys.platform == "darwin":
            self._api.ReqUserLogin(_req, 0, 0, "")
        else:
            self._api.ReqUserLogin(_req, 0)

    def OnRspUserLogin(
            self,
            pRspUserLogin: tdapi.CThostFtdcRspUserLoginField,
            pRspInfo: tdapi.CThostFtdcRspInfoField,
            nRequestID: int,
            bIsLast: bool,
    ):
        """登录响应"""
        if pRspInfo:
            print("登录响应", pRspInfo.ErrorID, pRspInfo.ErrorMsg)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:    python demo_td <frontaddr> <userid> <password>")
        exit(-1)

    FrontAddr = sys.argv[1]
    userid = sys.argv[2]
    password = sys.argv[3]

    spi = CTdSpiImpl()
    time.sleep(1)
    input("################# 按任意键退出 \n")
