from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MultiMatch


# Connect to Elasticsearch
connections.create_connection(hosts=['http://192.168.1.155:9200/'])

# Define an Elasticsearch Index
class DocumentIndex(Document):
    title = Text()
    description = Text()
    created_at = Date()

    class Index:
        name = 'documents'

# Initialize the index
DocumentIndex.init()

# Function to index a document  
def index_document(instance):
    obj = DocumentIndex(
        meta={'id': instance.id},
        title=instance.title,
        description=instance.description,
        created_at=instance.created_at,
    )
    obj.save()

# Function to search documents
def search_documents(query):
    q = MultiMatch(query=query , fields=['title', 'description'] , fuzziness="AUTO" )
    return DocumentIndex.search().query(q)
