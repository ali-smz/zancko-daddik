from django.http import JsonResponse
from .elasticsearch import ElasticModel
from django.conf import settings

def elasticsearch_insert_read(request):
    es_model = ElasticModel()  
    query = request.GET.get('q', '')
    index = request.GET.get('index', None)
    fuzzy = request.GET.get('fuzzy', 'false').lower() == 'true'
    
    if query:
        results = es_model.search_data(query, index=index, fuzzy=fuzzy)
    else:
        results = []
    
    return JsonResponse(results, safe=False)
