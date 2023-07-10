import bottle
from bottle import abort, request, route, response, run
from json import dumps as py2json


def checkLogin(username, password):

    return 1
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'
        response.headers['Access-Control-Expose-Headers'] = 'num-pages'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@route('/login', method=['POST', 'OPTIONS'])
@route('/login/', method=['POST', 'OPTIONS'])
@enable_cors
def login_post():
    # [0] do not cache content on client side
    response.set_header('Cache-Control', 'no-cache')

    # [1] get JSON document posted from the browser
    json_document = request.json
    username = str(json_document['userName'])
    password = str(json_document['passWord'])

    # remove cookie
    try:
        response.delete_cookie('account_type')
    except Exception as _:
        pass

    # [2] verify username & password
    user_id = checkLogin(username, password)

    if user_id is None:
        abort(401,"failed")


    else:
        # [2.1] set cookie
        response.set_cookie('user_id', user_id, secret='kevin')



        # [2.4] return success
        return py2json({'login_return_code': 0, 'days_to_account_expiry': 10})


@route('/login_hello', method=['Get', 'OPTIONS'])
@route('/login_hello/', method=['Get', 'OPTIONS'])
def login_post_hello():
    return "new data api"


if __name__ == "__main__":
     run(host='0.0.0.0', port=80, debug=True)

