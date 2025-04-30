"""
事件处理模块，为连接器提供事件发布/订阅功能
"""

class EventHandler:
    """
    事件处理类，实现发布/订阅模式
    """
    
    def __init__(self):
        """
        初始化事件处理器
        """
        self._subscribers = {}
    
    def subscribe(self, event_type, callback):
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type, callback):
        """
        取消订阅事件
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
    
    def publish(self, event_type, data=None):
        """
        发布事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(event_type, data)
