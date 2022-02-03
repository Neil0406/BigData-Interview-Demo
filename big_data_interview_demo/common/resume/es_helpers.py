from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from config import sensitive

es_config = sensitive.ES

class EsDemo():
    def __init__(self):
        hosts = es_config['HOSTS']
        port = es_config['PORT']
        user = es_config['USER'] + ':' +es_config['PASSWORD']
        self.traver_index = es_config['TRAVEL_INDEX']
        self.es = Elasticsearch(hosts=hosts, port=port, http_auth=user)

    def get_data_type_list(self):
        query = {
        "aggs": {
            "2": {
            "terms": {
                "field": "dataType",
                "order": {
                "_count": "desc"
                },
                "size": 100
                    }
                    }
                },
                "size": 0,
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                    "must": [],
                    "filter": [
                        {
                        "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        result = self.es.search(index=self.traver_index, body=query)
        return result['aggregations']['2']['buckets']

    def get_search_data(self, geo, data_type, distance):
        lat = geo['lat']
        lon = geo['lon']
        distance = distance + 'km'
        query ={                
                #距離排序 / 回傳 
                "sort": [{
                    "_geo_distance": {
                        "baseInfo.location": {
                            "lat": lat,
                            "lon": lon
                        },
                        "unit": "m",                   #回傳 公尺m 公里km
                            "distance_type": "arc",
                            "order": "asc"
                        }
                }],
                    "query": {
                        "bool": {
                            "must": {
                                "match": {
                                    'dataType':data_type
                                }
                            },
                            "filter": [{
                                "geo_distance": {
                                    "distance": distance,
                                    "baseInfo.location": {
                                        "lat": lat,
                                        "lon": lon
                                    }
                                }
                            }]
                        }
                    }
                }
        ret = self.es.search(index=self.traver_index, body=query, size=100)
        if len(ret['hits']['hits']) != 0:
            return ret['hits']['hits']
        else:
            return 0
        
    def get_city_list(self):
        query = {
        "aggs": {
            "2": {
            "terms": {
                "field": "baseInfo.region",
                "order": {
                "_count": "desc"
                },
                "size": 100
                    }
                    }
                },
                "size": 0,
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                    "must": [],
                    "filter": [
                        {
                        "match_all": {}
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            }
        }
        result = self.es.search(index=self.traver_index, body=query)
        result = list(map(lambda x: x['key'] , result['aggregations']['2']['buckets']))
        return result

    def activity_search(self, city, start_time, end_time):
        start_time = datetime.strptime(start_time, "%Y-%m-%d")
        start_time = start_time.timestamp()
        query = {
            'query':{
                'bool':{
                    'must':[
                        {'match_phrase':{'baseInfo.region':city}},
                    ]  
                    ,
                    'filter':[
                        {'match_phrase':{'dataType':'ACTIVITY'}},
                        {'range':{'activity.startTime':{'gte':int(start_time)}}},
                    ]
                }
            }
        }
        if end_time != '':
            end_time = datetime.strptime(end_time, "%Y-%m-%d")
            end_time = end_time.timestamp()
            query['query']['bool']['filter'][1]['range']['activity.startTime'].update({'lte':int(end_time)})
            #query['query']['bool']['filter'].append({'range':{'activity.endTime':{'lte':int(end_time)}}})
        ret = helpers.scan(self.es, index=self.traver_index, query=query)
        data = [i for i in ret]
        data = sorted(data, key=lambda k: k['_source']['activity']['startTime']) 
        for i in data:
            i['_source']['activity']['startTime'] = datetime.fromtimestamp(i['_source']['activity']['startTime']).strftime("%Y/%m/%d")
            i['_source']['activity']['endTime'] = datetime.fromtimestamp(i['_source']['activity']['endTime']).strftime("%Y/%m/%d")
            region = i['_source']['baseInfo']['region']
            district = i['_source']['baseInfo']['district']
            try:
                if region in i['_source']['baseInfo']['address']:
                    i['_source']['baseInfo']['address'] = i['_source']['baseInfo']['address'].replace(region,'')
            except:
                i['_source']['baseInfo']['address'] = ''
            try:
                if district in i['_source']['baseInfo']['address']:
                    i['_source']['baseInfo']['address'] = i['_source']['baseInfo']['address'].replace(district,'')
            except:
                i['_source']['baseInfo']['address'] = ''
            try:
                i['_source']['hashtag'] = ','.join(i['_source']['hashtag'])
            except:
                pass
        return data

    def store_exact_search(self, city, store_search):
        query = {
            "query": {
                "bool": {
                    "must": [{"match_phrase": {"baseInfo.name": store_search}}],
                    "filter": [
                        # {"match_phrase": {"dataType": "STORE"}},
                        {"match_phrase": {"baseInfo.region":city}}
                    ]
                }
            }
        }
        ret = self.es.search(index=self.traver_index, body=query, size=100)
        l = []
        if len(ret['hits']['hits']) != 0:
            for i in ret['hits']['hits']:
                try:
                    region = i['_source']['baseInfo']['region']
                    district = i['_source']['baseInfo']['district']
                    if region in i['_source']['baseInfo']['address']:
                        i['_source']['baseInfo']['address'] = i['_source']['baseInfo']['address'].replace(region,'')
                    if district in i['_source']['baseInfo']['address']:
                        i['_source']['baseInfo']['address'] = i['_source']['baseInfo']['address'].replace(district,'')
                    l.append(i)
                except:
                    pass
        return l

    def store_fuzzy_search(self, city, store_search):
        store_search = store_search.split(',')
        query = {
            "query": {
                "bool": {
                    "should": [
                    ],
                    "filter": [
                        {"match_phrase": {"baseInfo.region":city}}
                    ]
                }
            }
        }
        for i in store_search:
            query['query']['bool']['should'].append({"match": {"baseInfo.name": i}})
        ret = self.es.search(index=self.traver_index, body=query, size=100)
        l = []
        if len(ret['hits']['hits']) != 0:
            for i in ret['hits']['hits']:
                try:
                    if i['_score'] > 5:
                        region = i['_source']['baseInfo']['region']
                        district = i['_source']['baseInfo']['district']
                        if region in i['_source']['baseInfo']['address']:
                            i['_source']['baseInfo']['address'] = i['_source']['baseInfo']['address'].replace(region,'')
                        if district in i['_source']['baseInfo']['address']:
                            i['_source']['baseInfo']['address'] = i['_source']['baseInfo']['address'].replace(district,'')
                        l.append(i)
                except:
                    pass
        return l


