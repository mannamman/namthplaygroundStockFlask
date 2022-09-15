from flask import Blueprint, render_template, abort, request, Response
from my_module.date_module import DateModule
from my_module.mongo_module import Mongo
from my_module.log_module import GunicornLogger
import json
import traceback

stock_page = Blueprint("stock_index", __name__, template_folder="templates")

date_module = DateModule()
mongo = Mongo()
logger = GunicornLogger()

@stock_page.route("/index", methods=["GET"])
def stock_index():
    global date_module
    global mongo
    global logger
    try:
        stock_list = json.dumps(mongo.get_stock_list())
        cur_date = date_module.get_cur_date()
        return render_template("stockIndex.html", max_date=cur_date, start_date=cur_date, stock_list=stock_list)
    except Exception:
        error = traceback.format_exc()
        logger.error_log(json.dumps(error))
        abort(400)

@stock_page.route("/day", methods=["POST"])
def stock_daily():
    global mongo
    try:
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
            subject=subject,
            result=json.dumps(cursor_json),
        )
    except Exception:
        error = traceback.format_exc()
        logger.error_log(json.dumps(error))
        abort(400)


@stock_page.route("/error", methods=["GET"])
def for_error():
    global logger
    try:
        a = 4/0
        return Response(response="error", status=200)
    except Exception:
        error = traceback.format_exc()
        logger.error_log(json.dumps(error))
        abort(400)