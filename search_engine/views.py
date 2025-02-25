from django.http import JsonResponse
from .elasticsearch import ElasticModel
from django.conf import settings
from .models import SearchTermHistory
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
        auth_header = request.headers.get('Authorization', None)
        print(auth_header)
        if request.user.is_authenticated:
            print('authenticated')
            SearchTermHistory.objects.create(
                user=request.user, 
                search_term=query,      
                search_date=now()    
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
    data = es_model.get_single_data(id, index)
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'data not found'}, status=404)


class SearchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        search_history = SearchTermHistory.objects.filter(user=user).order_by('-search_date')

        history_data = [
            {
                'search_term': history_item.search_term,
                'search_date': history_item.search_date
            }
            for history_item in search_history
        ]

        return Response({'history': history_data}, status=status.HTTP_200_OK)