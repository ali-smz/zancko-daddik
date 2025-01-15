from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer
from .elasticsearch import index_document, search_documents

class DocumentCreateAPIView(APIView):
    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            # Index the document in Elasticsearch
            index_document(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        results = search_documents(query)
        return Response([hit.to_dict() for hit in results])
