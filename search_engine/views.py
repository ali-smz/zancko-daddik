# from django.shortcuts import render

# # Create your views here.

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Document
# from .serializers import DocumentSerializer
# from .elasticsearch import index_document, search_documents

# class DocumentCreateAPIView(APIView):
#     def post(self, request):
#         serializer = DocumentSerializer(data=request.data)
#         if serializer.is_valid():
#             document = serializer.save()
#             # Index the document in Elasticsearch
#             index_document(document)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DocumentSearchAPIView(APIView):
#     def get(self, request):
#         query = request.query_params.get('query', '')
#         results = search_documents(query)
#         return Response([hit.to_dict() for hit in results])






from django.http import JsonResponse
from .elasticsearch import ElasticModel
from django.conf import settings

def elasticsearch_insert_read(request):
    es_model = ElasticModel()
    es_model.create_index()
    data = [
        {
        'name': 'Sample Data',
        'description': 'This is a sample data entry for Elasticsearch.'
        } ,
        {
        'name': 'Sample Data 2',
        'description': 'This is a sample data entry for Elasticsearch 2222.'
        } ,

    ]
    for data in data :
        es_model.insert_data(data)
    
    # Read data
    results = es_model.read_data()
    
    return JsonResponse(results, safe=False)
