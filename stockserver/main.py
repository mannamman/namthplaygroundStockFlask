from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, Response
from pages.stock import stock_page
from middleware.common import corsMiddleware

app = Flask(__name__)

# cors 미들웨어 등록
app.wsgi_app = corsMiddleware(app.wsgi_app)
# blueprint 등록
app.register_blueprint(stock_page, url_prefix="/stock")

@app.route("/ping", methods=["GET"])
def ping():
    return Response(response="pong", status=200)

if(__name__ == "__main__"):
    app.run(debug=True, host=os.getenv("FLASK_DEV_HOST"), port=int(os.getenv("FLASK_DEV_PORT")))
