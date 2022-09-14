from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, make_response, Response
from pages.hello import gretting_page
from pages.stock import stock_page


app = Flask(__name__)
app.register_blueprint(gretting_page, url_prefix="/blue")
app.register_blueprint(stock_page, url_prefix="/stock")

@app.route("/ping", methods=["GET", "POST"])
def ping():
    return make_response(Response(response="pong", status=200))


if(__name__ == "__main__"):
    # gunicorn --bind 127.0.0.1:8880 --workers 1 --threads 4 --timeout 0 main:app
    app.run(debug=True, host=os.getenv("FLASK_DEV_HOST"), port=int(os.getenv("FLASK_DEV_PORT")))