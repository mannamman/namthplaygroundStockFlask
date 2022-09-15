import yfinance
import datetime
from typing import Tuple, List
import pandas as pd

class YFin:
    def __init__(self) -> None:
        self.history_period = "1d"
        self.date_format = "%Y-%m-%d"

    def __new__(cls):
        if(not hasattr(cls, "instance")):
            cls.instance = super(YFin, cls).__new__(cls)
        return cls.instance

    def get_real_stock(
            self,
            stock_code: str,
            start: datetime.datetime,
            end: datetime.datetime
        ) -> Tuple[List[float], List[str]]:

        if(not isinstance(start, datetime.datetime) or not isinstance(end, datetime.datetime)):
            raise Exception(f"start or end type is not datetime.\nstart: {type(start)} end: {type(end)}")
        
        start = start.isoformat().split("T")[0]
        end = end.isoformat().split("T")[0]

        stock_yf = yfinance.Ticker(stock_code)

        stock_history: pd.DataFrame = stock_yf.history(period=self.history_period, start=start, end=end)
    
        close_prices = stock_history["Close"].tolist()
        close_dates = stock_history.index.tolist()
        close_dates = [datetime.datetime.strftime(close_date, self.date_format) for close_date in close_dates]
        
        return (close_prices, close_dates)

if(__name__ == "__main__"):
    yfin = YFin()
    start = datetime.datetime(2022, 2, 28)
    end = datetime.datetime(2022, 3, 7)
    subejct = "APPL"
    p,d = yfin.get_real_stock(subejct, start, end)
    print(p,d)
    print(len(p))