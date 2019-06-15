from .views import jwt_refresh_token
import json


class AuthMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        return response
        # import pdb;pdb.set_trace()
        # if request.user.is_authenticated and request.:
        # 	token = jwt_refresh_token(request)
	       #  dict_cust = eval(response.__dict__.get('_container')[0])
	       #  dict_cust.update({"token":token.decode('ASCII')})
	       #  response.__dict__.get('_container')[0] = json.dumps(dict_cust).encode('ASCII')

