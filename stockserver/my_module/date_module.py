import pytz
import datetime

class DateModule:
    def __init__(self) -> None:
        self.KST = pytz.timezone('Asia/Seoul')
        self.date_format = "%Y-%m-%d"
        self.datetime_format = "%Y-%m-%d %H:%M:%S"
        
    
    def __new__(cls):
        if(not hasattr(cls, "instance")):
            cls.instance = super(DateModule, cls).__new__(cls)
        return cls.instance
    

    def get_cur_date(self) -> str:
        return pytz.utc.localize(datetime.datetime.utcnow()).astimezone(self.KST).strftime(self.date_format)
