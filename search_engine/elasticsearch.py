from elasticsearch import Elasticsearch
from django.conf import settings


class ElasticModel:
    def __init__(self, index='tamin_ejtemaei'):
        self.client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])
        self.index = index
    
    def search_data(self, query, fields=None, index=None):
        search_index = index or self.index
        if fields is None and search_index == 'tamin_ejtemaei':
            fields = ["Title", "AttachmentText", "TitleNumber", "Subject", "AttachmentLink", "TitleDate", "ApprovalAuthority", "Organization"]
            
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": fields,
                    "fuzziness": "AUTO"
                }
            }
        }
        response = self.client.search(index=search_index, body=search_body)
        return response['hits']['hits']