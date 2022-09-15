import pymongo
from pymongo.cursor import Cursor
import os
import datetime
from typing import Dict, List, Tuple
from bson.json_util import dumps
from my_module.yfin_module import YFin
import copy
import time
import json

"""
RDBMS	    Mongo DB
Database	Database
Table	    Collection
Row	        Document
Index	    Index
DB server	Mongod
DB client	mongo
"""

class Mongo:
    def __init__(self):
        ip = os.getenv("MONGO_HOST")
        port = os.getenv("MONGO_PORT")
        user = os.getenv("MONGO_USER")
        passwd = os.getenv("MONGO_PASSWD")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # stock db 설정
        self.db = self.client["stock"]
        self.collection = self.db["en"]
        # stock 리스트 가져오기
        self.stock_list_collection = self.db["stockList"]
        self._update_stock_list()
        self.stock_change = False
        # yfin 모듈 초기화
        self.yfin = YFin()
    
    def __new__(cls):
        if(not hasattr(cls, "instance")):
            cls.instance = super(Mongo, cls).__new__(cls)
        return cls.instance
    
    def _subject_map(self, subject: str) -> str:
        for stock_info in self.stock_list:
            if(stock_info["stock_name"] == subject):
                return stock_info["stock_code"]
        raise ValueError(f"Unknown stock name {subject}!")
    
    def _update_stock_list(self) -> None:
        cursor = self.stock_list_collection.find()
        cursor_list = list(cursor)
        stock_str = dumps(cursor_list)
        stock_list = json.loads(stock_str)
        self.stock_list = stock_list

    def _calc_day_static(self, cursor: Cursor) -> Tuple[Dict[str,str], List[dict]]:
        range_dict = {
            "range_positive_cnt": 0,
            "range_negative_cnt": 0,
            "ragne_total_cnt": 0
        }
        day_results = []

        for query_result in cursor:
            sentiment_results = query_result["sentiment"]
            day_positive_cnt = 0
            day_negative_cnt = 0
            day_total_cnt = 0
            day_dict = {
                "createdAt": query_result["createdAt"].isoformat().split("T")[0]
            }
            for sentiment_result in sentiment_results:
                day_total_cnt += 1
                positive = sentiment_result["positive"]
                negative = sentiment_result['negative']
                if((positive > negative) and (positive > 0.2)):
                    day_positive_cnt += 1
                elif((negative > positive) and (negative > 0.2)):
                    day_negative_cnt += 1
                else:
                    if((negative * 10) < positive):
                        day_positive_cnt += 1
                    elif((positive * 10) < negative):
                        day_negative_cnt += 1
            day_dict["positive_cnt"] = day_positive_cnt
            day_dict["negative_cnt"] = day_negative_cnt
            day_dict["total_cnt"] = day_total_cnt
            range_dict["ragne_total_cnt"] += day_total_cnt
            range_dict["range_negative_cnt"] += day_negative_cnt
            range_dict["range_positive_cnt"] += day_positive_cnt
            day_results.append(day_dict)
        return range_dict, day_results

    def get_stock_list(self) -> List[dict]:
        if(self.stock_change):
            self._update_stock_list()
            self.stock_change = False
        return self.stock_list

    def add_stock_list(self, stock_infos: List[Dict[str,str]]) -> None:
        cur = round(time.time())
        for stock_info in stock_infos:
            stock_info["createdAt"] = cur
        self.stock_list_collection.insert_many(stock_infos)

    def get_range_data(self, subject: str, start: str):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = start + datetime.timedelta(days=30)

        query = {
          "subject": subject,
          "$and": [{ "createdAt": { "$gte": start } }, { "createdAt": { "$lte": end } }],
        }
        cursor = self.collection.find(query, {"uuid": 0})
        res_cursor = copy.copy(cursor)

        range_dict, day_results = self._calc_day_static(cursor)

        stock_code = self._subject_map(subject)
        close_prices, close_dates = self.yfin.get_real_stock(stock_code, start, end)

        res_cursor = list(res_cursor)
        cursor_json = dumps(res_cursor, indent=4)
        return range_dict, day_results, close_prices, close_dates, cursor_json

if(__name__ == "__main__"):
    from dotenv import load_dotenv
    load_dotenv()
    m = Mongo()
