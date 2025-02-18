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

    def search_data(self, query, fields=None, fuzzy=True, index=None):
        if fields is None:
            fields = ["Title", "AttachmentText", "TitleNumber", "Subject", "AttachmentLink", "TitleDate", "ApprovalAuthority", "Organization"]

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
            }
        }

        print(index or self.index)
        print(search_body)
        print(fuzzy)
        
        response = self.client.search(index=index or self.index, body=search_body)
        return response['hits']['hits']
