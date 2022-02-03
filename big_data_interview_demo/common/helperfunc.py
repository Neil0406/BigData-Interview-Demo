
from datetime import datetime, time
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status as http_status
from common import errorcode
from common.exceptions import RequestInputParserError
from big_data_interview_demo import settings

IS_DEBUGGING = getattr(settings, 'DEBUG', False)


def api_response(result='Success', status=http_status.HTTP_200_OK, code=errorcode.OK, error=None, **kargs):
    if error or code != errorcode.OK:
        print(f'[Error]: api_response ---> [Info]: {error}')
    else:
        pass

    # 如果 code 不為 0 強制將 http_status 從 200 改為 400
    if code != errorcode.OK and status == http_status.HTTP_200_OK:
        status = http_status.HTTP_400_BAD_REQUEST

    if IS_DEBUGGING and error and type(result) is str:
        result += ": " + str(error)

    content = {}
    if type(result) is not list:
        if result is None:
            content["result"] = []
        elif type(result) is dict and "token" in result:
            content = result
        else:
            content["result"] = [result]
    else:
        content["result"] = result

    if "code" not in content:
        content["code"] = code
    return Response(content, status=status, content_type='application/json', **kargs)


def get_request_input(request, method='POST', required_data=[]):
    if method == 'GET':
        input_data = dict(request.query_params)
    else:
        input_data = dict(request.data)
    if "application/json" not in request.content_type.lower():
        for key in input_data:
            if type(input_data[key]) is list and len(input_data[key]) == 1:
                input_data[key] = input_data[key][0]

    for item in required_data:
        if item not in input_data:
            raise RequestInputParserError("Required data not found: {0}".format(item))

    # Dirty fix
    if request._read_started:
        request._read_started = False
    return input_data

def result_process(data):
    ret = []
    if type(data) != list:
        ret.append(data)
    else:
        ret = data
    return ret