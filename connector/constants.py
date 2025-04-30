"""
CTP连接器常量定义文件
"""

CONNECTOR_STATUS_DISCONNECTED = 0  # 未连接
CONNECTOR_STATUS_CONNECTING = 1    # 连接中
CONNECTOR_STATUS_CONNECTED = 2     # 已连接
CONNECTOR_STATUS_LOGGED_IN = 3     # 已登录
CONNECTOR_STATUS_READY = 4         # 就绪

EVENT_TYPE_CONNECTED = "connected"                # 连接成功
EVENT_TYPE_DISCONNECTED = "disconnected"          # 断开连接
EVENT_TYPE_LOGIN_SUCCESS = "login_success"        # 登录成功
EVENT_TYPE_LOGIN_FAILED = "login_failed"          # 登录失败
EVENT_TYPE_AUTH_SUCCESS = "auth_success"          # 认证成功
EVENT_TYPE_AUTH_FAILED = "auth_failed"            # 认证失败
EVENT_TYPE_SETTLEMENT_CONFIRMED = "settlement_confirmed"  # 结算单确认
EVENT_TYPE_MARKET_DATA = "market_data"            # 市场数据
EVENT_TYPE_ORDER_STATUS = "order_status"          # 订单状态
EVENT_TYPE_TRADE = "trade"                        # 成交信息
