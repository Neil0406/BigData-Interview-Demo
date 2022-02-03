from common import errorcode
from popular_content.models import PopularContent, PopularContentSource
from django.forms import model_to_dict
from common.helperfunc import api_response
from rest_framework import status as http_status

class PopularContentModel():
    def get_popular_content(self):
        info = ''
        result = []
        try:
            popular_content = PopularContent.objects.all().filter(soft_delete=False)
            for i in popular_content:
                dic = model_to_dict(i)
                del dic['soft_delete']
                dic['source'] = list(map(lambda x: {'source_type': x.source_type, 'source_name':x.source_name, 'source_path':x.source_path}, \
                                    PopularContentSource.objects.filter(popular_content_id = i.id, soft_delete=False))
                                )
                result.append(dic)
            res = api_response(result)
        except Exception as e:
            info = str(e)
            res = api_response(info, http_status.HTTP_500_INTERNAL_SERVER_ERROR, errorcode.INTERNAL_SERVER_ERROR)
        return res
    
    def create_popular_content(self, input_data):
        info = ''
        try:
            title = input_data['title']
            content = input_data['content']
            source = input_data['source']
            content_id = PopularContent.objects.create(**{'title': title, 'content':content}).id
            source_create = []
            for i in source:
                dic = {
                        'source_type' : i['source_type'],
                        'source_name' : i['source_name'],
                        'source_path' : 'https://popular_content.s3.ap-northeast-1.amazonaws.com/source/',
                        'popular_content_id': content_id
                    }
                source_create.append(PopularContentSource(**dic))
            PopularContentSource.objects.bulk_create(source_create)   
            info = 'Create Popular Content'
            res = api_response(info)
        except Exception as e:
            info = str(e)
            res = api_response(info, http_status.HTTP_500_INTERNAL_SERVER_ERROR, errorcode.INTERNAL_SERVER_ERROR)
        return res
        
    def update_popular_content(self, input_data):
        info = ''
        try:
            id = input_data['id']
            title = input_data['title']
            content = input_data['content']
            source = input_data['source']
            
            popular_content = PopularContent.objects.filter(id=id)
            if popular_content.count() != 0:
                popular_content.update(**{'title': title, 'content':content})
                content_id = popular_content[0].id
                PopularContentSource.objects.filter(popular_content_id=content_id).delete()
                source_create = []
                for i in source:
                    dic = {
                            'source_type' : i['source_type'],
                            'source_name' : i['source_name'],
                            'source_path' : 'https://popular_content.s3.ap-northeast-1.amazonaws.com/source/',
                            'popular_content_id': content_id
                        }
                    source_create.append(PopularContentSource(**dic))
                PopularContentSource.objects.bulk_create(source_create)   
         
                info = 'Update Popular Content'
                res = api_response (info)
            else:
                info = 'Data Not Exists'
                res = api_response (info, http_status.HTTP_400_BAD_REQUEST, errorcode.DATA_NOT_EXISTS)
        except Exception as e:
            info = str(e)
            res = api_response (info, http_status.HTTP_400_BAD_REQUEST, errorcode.DATA_NOT_EXISTS)
        return res
    
    def delete_popular_content(self, input_data):
        info = ''
        try:
            content_id = input_data['id']
            popular_content = PopularContent.objects.filter(id=content_id)
            if popular_content.count() != 0:
                popular_content.delete()
                info = 'Delete Popular Content'
                res = api_response(info)
            else:
                info = 'Data Not Exists'
                res = api_response (info, http_status.HTTP_400_BAD_REQUEST, errorcode.DATA_NOT_EXISTS)
        except Exception as e:
            info = str(e)
            res = api_response (info, http_status.HTTP_400_BAD_REQUEST, errorcode.DATA_NOT_EXISTS)
        return res