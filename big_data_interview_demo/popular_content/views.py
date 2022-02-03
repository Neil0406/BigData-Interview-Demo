from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common import errorcode
from common.helperfunc import api_response
from common.decorators import key_check
from rest_framework import status as http_status
from popular_content.popular_content_model import PopularContentModel
from popular_content.enum import SourceType

popular_content_model = PopularContentModel()

class PopularContent(APIView):
    
    required_data = []
    @key_check(required_data)
    @swagger_auto_schema(operation_summary='取得熱門文章')
    def get(self, request, input_data):
        try:
            res = popular_content_model.get_popular_content()
            return res
        except Exception as e:
            msg = "Get popular content failed with error"
            return api_response(msg, http_status.HTTP_500_INTERNAL_SERVER_ERROR, errorcode.INTERNAL_SERVER_ERROR,
                                error=e)
    
    required_data = ['title', 'content', 'source']
    @key_check(required_data)
    @swagger_auto_schema(
        operation_summary='新增熱門文章',
        operation_description='檔案上傳格式為base64 (Demo會先將其功能關閉)',
        responses = {'200': openapi.Response(
            description = 'message',
            examples={'application/json':{"resault":["Create Popular Content"],"code":0}}
        )},      
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content', 'source'],
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章標題'
                ),              
                'content': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章內容'
                ),
                'source': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description = '資源',
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        required=['source_type', 'source_name', 'source_upload'],
                        properties={
                            'source_type': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='資源類型 (0: 圖片 / 1: 影片)'
                            ),      
                            'source_name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='資源名稱'
                            ),
                            'source_upload': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='檔案上傳(base64) / 測試請填空字串'
                            ),
                        }
                    )
                )
            }
        )
    )
    def post(self, request, input_data):
        try:
            source_type = [i.value for i in SourceType]
            for i in input_data['source']:
                if 'source_type' not in i:
                    return api_response("Required data not found: source_type", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
                elif 'source_name' not in i:
                    return api_response("Required data not found: source_name", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
                elif 'source_upload' not in i:
                    return api_response("Required data not found: source_upload", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
                if i['source_type'] not in source_type:
                    return api_response("source_type error", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
            res = popular_content_model.create_popular_content(input_data)
            return res
        except Exception as e:
            msg = "Post popular content failed with error"
            return api_response(msg, http_status.HTTP_500_INTERNAL_SERVER_ERROR, errorcode.INTERNAL_SERVER_ERROR,
                                error=e)
            
    required_data = ['id', 'title', 'content', 'source']
    @key_check(required_data)
    @swagger_auto_schema(
        operation_summary='更新熱門文章',
        operation_description='檔案上傳格式為base64 (Demo會先將其功能關閉)',
        responses = {'200': openapi.Response(
            description = 'message',
            examples={'application/json':{"resault":["Update Popular Content"],"code":0}}
        )},      
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'title', 'content', 'source'],
            properties={
                'id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章ID'
                ),  
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章標題'
                ),              
                'content': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章內容'
                ),
                'source': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description = '資源',
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        required=['source_type', 'source_name', 'source_upload'],
                        properties={
                            'source_type': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='資源類型 (0: 圖片 / 1: 影片)'
                            ),      
                            'source_name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='資源名稱'
                            ),
                            'source_upload': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='檔案上傳(base64) / 測試請填空字串'
                            ),
                        }
                    )
                )
            }
        )
    )
    def put(self, request, input_data):
        try:
            source_type = [i.value for i in SourceType]
            for i in input_data['source']:
                if 'source_type' not in i:
                    return api_response("Required data not found: source_type", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
                elif 'source_name' not in i:
                    return api_response("Required data not found: source_name", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
                elif 'source_upload' not in i:
                    return api_response("Required data not found: source_upload", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
                if i['source_type'] not in source_type:
                    return api_response("source_type error", http_status.HTTP_400_BAD_REQUEST, errorcode.BADREQUEST)
            res = popular_content_model.update_popular_content(input_data)
            return res
        except Exception as e:
            msg = "Update popular content failed with error"
            return api_response(msg, http_status.HTTP_500_INTERNAL_SERVER_ERROR, errorcode.INTERNAL_SERVER_ERROR,
                                error=e)
            
    required_data = ['id']
    @key_check(required_data)
    @swagger_auto_schema(
        operation_summary='刪除熱門文章',
                responses = {'200': openapi.Response(
            description = 'message',
            examples={'application/json':{"resault":["Delete Popular Content"],"code":0}}
        )},      
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章ID'
                )
            }
        )
    )
    def delete(self, request, input_data):
        try:
            res = popular_content_model.delete_popular_content(input_data)
            return res
        except Exception as e:
            msg = "Delete popular content failed with error"
            return api_response(msg, http_status.HTTP_500_INTERNAL_SERVER_ERROR, errorcode.INTERNAL_SERVER_ERROR,
                                error=e)
    
            
            
popular_content = PopularContent.as_view()