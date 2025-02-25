from django.http import JsonResponse
from .elasticsearch import ElasticModel
from django.conf import settings

def elasticsearch_insert_read(request):
    es_model = ElasticModel()  
    query = request.GET.get('q', '')
    index = request.GET.get('index', None)
    fuzzy = request.GET.get('fuzzy', 'false').lower() == 'true'
    
    try:
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
    except ValueError:
        page = 1
        size = 10

    if query:
        results = es_model.search_data(
            query, 
            index=index, 
            fuzzy=fuzzy,
            page=page,
            size=size
        )
    else:
        results = {
            'hits': [],
            'total': 0,
            'page': page,
            'size': size,
            'total_pages': 0
        }
    
    return JsonResponse(results, safe=False)

def get_single_data(request):
    es_model = ElasticModel()
    id = request.GET.get('id', None)
    if not id:
        return JsonResponse({'error': 'id is required'}, status=400)
    index = request.GET.get('index', None)
    print(index , id)
    data = es_model.get_single_data(id, index)
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'data not found'}, status=404)

