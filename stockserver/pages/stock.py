from flask import Blueprint, render_template, abort, request, Response
from my_module.date_module import DateModule
from my_module.mongo_module import Mongo
import json

stock_page = Blueprint("stock_index", __name__, template_folder="templates")

date_module = DateModule()
mongo = Mongo()

@stock_page.route("/index", methods=["GET"])
def stock_index():
    global date_module
    cur_date = date_module.get_cur_date()
    return render_template("stockIndex.html", max_date=cur_date, start_date=cur_date)

@stock_page.route("/day", methods=["POST", "GET"])
def stock_day():
    global mongo
    if(request.method == "GET"):
        return Response(response="barsws", status=200)
    subject = request.form["subject"]
    start = request.form["start"]
    range_dict, day_results, close_prices, close_dates, cursor_json = mongo.get_range_data(subject=subject, start=start)
    return render_template("dayStatistics.html", 
        total_cnt=range_dict["ragne_total_cnt"],
        positive_cnt=range_dict["range_positive_cnt"],
        negative_cnt=range_dict["range_negative_cnt"],
        day_statistics=json.dumps(day_results),
        close_prices=close_prices,
        close_dates=close_dates,
        subejct=subject,
        result=cursor_json,
    )
