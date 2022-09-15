from werkzeug.wrappers import Request, Response

class corsMiddleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if(request.method == 'OPTIONS'):
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': ["GET","POST"],
                'Access-Control-Allow-Headers': ['Content-Type', 'Authorization'],
                'Access-Control-Max-Age': '3600'
            }
            res = Response(status=204, response="", headers=headers, mimetype= "text/plain")
            return res(environ, start_response)
        
        return self.app(environ, start_response)
