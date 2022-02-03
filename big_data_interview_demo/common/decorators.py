from functools import wraps
from common import errorcode
from common.exceptions import RequestInputParserError
from common.helperfunc import get_request_input, api_response
from rest_framework import status as http_status

def key_check(required_data=None):
    if required_data is None:
        required_data = []
    def f(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            request = args[0]
            try:
                input_data = get_request_input(request, request.method, required_data)
                res = func(self, request, input_data)
            except RequestInputParserError as e:
                msg = "Request input parse error"
                res = api_response(msg, http_status.HTTP_400_BAD_REQUEST, errorcode.REQUEST_INPUT_PARSE_ERROR, error=e)
            except Exception as e:
                msg = "UNKNOWN ERROR"
                res = api_response(msg, http_status.HTTP_500_INTERNAL_SERVER_ERROR, errorcode.INTERNAL_SERVER_ERROR, error=e)
            return res

        return wrapper
    return f

