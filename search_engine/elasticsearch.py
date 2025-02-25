from elasticsearch import Elasticsearch
from django.conf import settings


class ElasticModel:
    def __init__(self):
        self.client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        self.index = 'tamin_ejtemaei'

    def create_index(self):
        if not self.client.indices.exists(index=self.index):
            self.client.indices.create(index=self.index)

    def insert_data(self, data):
        self.client.index(index=self.index, document=data)

    def search_data(self, query, fields=None, fuzzy=True, index=None, page=1, size=10):
        if fields is None:
            fields = ["Title", "AttachmentText", "TitleNumber", "Subject", "AttachmentLink", "TitleDate", "ApprovalAuthority", "Organization"]

        from_ = (page - 1) * size

        multi_match = {
            "query": query,
            "type": "best_fields",
            "fields": fields
        }

        if fuzzy:
            multi_match["fuzziness"] = "AUTO"
        else:
            multi_match["operator"] = "AND"
        
        search_body = {
            "query": {
                "multi_match": multi_match
            },
            "from": from_,
            "size": size
        }
        
        response = self.client.search(index=index or self.index, body=search_body)
        
        # Return both hits and total count
        return {
            'hits': response['hits']['hits'],
            'total': response['hits']['total']['value'],
            'page': page,
            'size': size,
            'total_pages': (response['hits']['total']['value'] + size - 1) // size
        }
    
    def get_single_data(self, id , index = None):
        try :
            response = self.client.get(index=index or self.index, id=id)
            return response['_source']
        except Exception as e:
            print(str(e))
            return None
