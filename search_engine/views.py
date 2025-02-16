from django.http import JsonResponse
from .elasticsearch import ElasticModel
from django.conf import settings

def elasticsearch_insert_read(request):
    es_model = ElasticModel()  
    # Check if the index exists, if not create it and insert data
    # if not es_model.client.indices.exists(index=es_model.index):
    #     es_model.create_index()
        # data = [
        #     {
        #         'name': 'Sample Data',
        #         'description': 'This is a sample data entry for Elasticsearch.'
        #     },
        #     {
        #         'name': 'Sample Data 2',
        #         'description': 'This is a sample data entry for Elasticsearch 2222.'
        #     },
        # ]
        # for entry in data:
        #     es_model.insert_data(entry)
    
    # Search data based on query parameters
    query = request.GET.get('q', '')
    if query:
        results = es_model.search_data(query)
    else:
        results = []
    
    return JsonResponse(results, safe=False)
