import logging
class GunicornLogger:
    def __init__(self) -> None:
        # error이 stdout같음
        self.gunicorn_logger = logging.getLogger('gunicorn.error')
        self.gunicorn_logger.setLevel(logging.DEBUG)
    
    def __new__(cls):
        if(not hasattr(cls, "instance")):
            cls.instance = super(GunicornLogger, cls).__new__(cls)
        return cls.instance
    
    def error_log(self, message):
        self.gunicorn_logger.log(logging.ERROR, message)
    
    def debug_log(self, message):
        self.gunicorn_logger.log(logging.DEBUG, message)
    
    def info_log(self, message):
        self.gunicorn_logger.log(logging.INFO, message)