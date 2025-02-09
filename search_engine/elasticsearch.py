from elasticsearch_dsl import Document, Text, Date
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MultiMatch



connections.create_connection(hosts=['http://192.168.30.6:9200'])


class DocumentIndex(Document):
    title = Text()
    description = Text()
    created_at = Date()

    class Index:
        name = 'documents'

DocumentIndex.init()

# Function to index a document  
def index_document(instance):
    obj = DocumentIndex(
        meta={'id': instance.id},
        id = instance.id ,
        title=instance.title,
        description=instance.description,
        created_at=instance.created_at,
    )
    obj.save()

# Function to search documents
def search_documents(query):
    q = MultiMatch(query=query , fields=['title', 'description'] , fuzziness="AUTO" )
    return DocumentIndex.search().query(q)
