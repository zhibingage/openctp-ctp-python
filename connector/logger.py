"""
日志模块，为连接器提供日志记录功能
"""
import os
import logging
import datetime

class Logger:
    """
    日志记录类，封装Python标准日志模块
    """
    
    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    DEFAULT_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] - %(message)s'
    
    @staticmethod
    def get_logger(name, level='info', log_file=None, log_format=None):
        """
        获取日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别，可选值：debug, info, warning, error, critical
            log_file: 日志文件路径，如果为None则输出到控制台
            log_format: 日志格式，如果为None则使用默认格式
        
        Returns:
            logging.Logger: 日志记录器
        """
        logger = logging.getLogger(name)
        
        logger.setLevel(Logger.LEVELS.get(level.lower(), logging.INFO))
        
        if logger.handlers:
            return logger
        
        formatter = logging.Formatter(log_format or Logger.DEFAULT_FORMAT)
        
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            handler = logging.FileHandler(log_file, encoding='utf-8')
        else:
            handler = logging.StreamHandler()
        
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
        return logger

def get_default_log_file(name):
    """
    获取默认日志文件路径
    
    Args:
        name: 日志名称
    
    Returns:
        str: 日志文件路径
    """
    today = datetime.datetime.now().strftime('%Y%m%d')
    
    log_dir = os.path.join(os.path.expanduser('~'), 'logs', 'ctp')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    return os.path.join(log_dir, f'{name}_{today}.log')
