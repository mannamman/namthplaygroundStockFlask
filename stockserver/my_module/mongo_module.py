import pymongo
from pymongo.cursor import Cursor
import os
import datetime
from uuid import uuid4
from typing import Dict, List, Tuple
from bson.json_util import dumps, loads
from my_module.yfin_module import YFin

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
        ip = os.getenv("MONGO_DEV_HOST")
        port = os.getenv("MONGO_PORT")
        user = os.getenv("MONGO_USER")
        passwd = os.getenv("MONGO_PASSWD")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # db 설정
        self.db = self.client["stock"]
        # table 고정(collection)
        self.collection = self.db["en"]
        self.yfin = YFin()

    def save_result(
            self,
            sentiment_results: List[Dict[str,any]],
            subject: str,
            kst: datetime.datetime
        ) -> None:

        sec = kst.second
        ms = kst.microsecond
        dt = datetime.timedelta(microseconds=ms, seconds=sec)
        rounded_kst = kst - dt

        doc_format = {
            "uuid" : uuid4(),
            "subject" : subject,
            "createdAt" : rounded_kst,
            "sentiment" : sentiment_results
        }

        self.collection.insert_one(doc_format)
    
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


    def get_range_data(self, subject: str, start: str):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = start + datetime.timedelta(days=30)
        subject = "tesla"
        query = {
          "subject": subject,
          "$and": [{ "createdAt": { "$gte": start } }, { "createdAt": { "$lte": end } }],
        }
        cursor = self.collection.find(query, {"uuid": 0})
        range_dict, day_results = self._calc_day_static(cursor)
        close_prices, close_dates = self.yfin.get_real_stock(subject, start, end)
        cursor_json = dumps(list(cursor), indent=4)
        return range_dict, day_results, close_prices, close_dates, cursor_json

            

if(__name__ == "__main__"):
    from dotenv import load_dotenv
    load_dotenv()
    m = Mongo().get_range_data(1,2,3)