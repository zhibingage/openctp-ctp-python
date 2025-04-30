"""
基础连接器接口定义
"""
from abc import ABC, abstractmethod
from .eventhandler import EventHandler
from .constants import *
from .logger import Logger, get_default_log_file

class BaseConnector(ABC):
    """
    基础连接器抽象类，定义连接器通用接口
    """
    
    def __init__(self):
        """
        初始化基础连接器
        """
        self._status = CONNECTOR_STATUS_DISCONNECTED
        self._event_handler = EventHandler()
        self._logger = None
    
    def init_logger(self, name, level='info', log_file=None, log_format=None):
        """
        初始化日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别，可选值：debug, info, warning, error, critical
            log_file: 日志文件路径，如果为None则使用默认路径
            log_format: 日志格式，如果为None则使用默认格式
        """
        if log_file is None:
            log_file = get_default_log_file(name)
        
        self._logger = Logger.get_logger(name, level, log_file, log_format)
        self._logger.info(f"Logger initialized. Level: {level}, File: {log_file}")
    
    @property
    def logger(self):
        """
        获取日志记录器
        
        Returns:
            logging.Logger: 日志记录器
        """
        return self._logger
    
    @property
    def status(self):
        """
        获取连接状态
        
        Returns:
            int: 连接状态码
        """
        return self._status
    
    @status.setter
    def status(self, value):
        """
        设置连接状态
        
        Args:
            value: 连接状态码
        """
        self._status = value
        if self._logger:
            self._logger.debug(f"Connector status changed to: {value}")
    
    def subscribe_event(self, event_type, callback):
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        self._event_handler.subscribe(event_type, callback)
        if self._logger:
            self._logger.debug(f"Subscribed to event: {event_type}")
    
    def unsubscribe_event(self, event_type, callback):
        """
        取消订阅事件
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        self._event_handler.unsubscribe(event_type, callback)
        if self._logger:
            self._logger.debug(f"Unsubscribed from event: {event_type}")
    
    def publish_event(self, event_type, data=None):
        """
        发布事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        self._event_handler.publish(event_type, data)
        if self._logger:
            self._logger.debug(f"Published event: {event_type}")
    
    @abstractmethod
    def connect(self):
        """
        连接到服务器
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """
        断开与服务器的连接
        """
        pass
    
    @abstractmethod
    def is_connected(self):
        """
        检查是否已连接
        
        Returns:
            bool: 是否已连接
        """
        pass
