from django.http import JsonResponse
from .elasticsearch import ElasticModel
from django.conf import settings
from .models import SearchTermHistory , Bookmark , Comment
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
from django.contrib.auth import get_user_model


def elasticsearch_insert_read(request):
    es_model = ElasticModel()
    query = request.GET.get('q', '')
    index = request.GET.get('index', None) 
    fuzzy = request.GET.get('fuzzy', 'false').lower() == 'true'

    try:
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
    except ValueError:
        page, size = 1, 10

    if not query:
        return JsonResponse({
            'hits': [], 'total': 0, 'page': page, 'size': size, 'total_pages': 0
        }, safe=False)

    results = es_model.search_data(query, index=index, fuzzy=fuzzy, page=page, size=size)

    auth_header = request.headers.get('Authorization', None)
    if auth_header and auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'],
                options={"verify_exp": True}
            )

            User = get_user_model()
            user = User.objects.only("id", "searchs").get(id=payload.get('user_id'))

            subscription = user.subscription.latest('end_date')
            SearchTermHistory.objects.create(user=user, search_term=query, search_date=now())

            if user.searchs < 7 and subscription.plan.name == "free":
                user.searchs += 1
                user.save(update_fields=["searchs"])

        except ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=401)

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
    

class BookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        index = request.data.get('index')
        record_id = request.data.get('record_id')

        if not record_id or not index:
            return JsonResponse({"error": "Missing record_id or index"}, status=400)

        bookmark, created = Bookmark.objects.get_or_create(user=user, index=index, record_id=record_id)

        if created:
            return JsonResponse({"message": "Bookmark created successfully"}, status=201)
        else:
            return JsonResponse({"message": "Bookmark already exists"}, status=200)
        
    def get(self , request):
        user = request.user
        es_model = ElasticModel()

        bookmarks = Bookmark.objects.filter(user=user).values("record_id" , "index")

        res = []
        for bookmark in bookmarks :
            record = es_model.get_single_data(bookmark['record_id'] , bookmark['index'])
            if record :
                res.append(record)
        
        return JsonResponse(res , status=200 , safe=False)
    
    def delete(self, request):
        user = request.user
        index = request.data.get('index')
        record_id = request.data.get('record_id')

        if not record_id or not index:
            return JsonResponse({"error": "Missing record_id or index"}, status=400)

        try:
            bookmark = Bookmark.objects.get(user=user, record_id=record_id, index=index)
            bookmark.delete()
            return JsonResponse({"message": "Bookmark removed successfully"}, status=200)
        except Bookmark.DoesNotExist:
            return JsonResponse({"error": "Bookmark not found"}, status=404)



class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
    
        user = request.user
        record_id = request.data.get("record_id")
        index = request.data.get("index") 
        body = request.data.get("body")
        rating = request.data.get("rating")

        if not record_id or not body or not index:
            return Response({"error": "Missing record_id or body or index"}, status=status.HTTP_400_BAD_REQUEST)

        if rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    return Response({"error": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Invalid rating value"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            user=user, record_id=record_id, index=index, body=body, rating=rating or 0
        )

        return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)

    def get(self, request):
    
        record_id = request.GET.get("record_id")
        index = request.GET.get("index")

        if not record_id or not index:
            return Response({"error": "Missing record_id or index"}, status=status.HTTP_400_BAD_REQUEST)

        comments = Comment.objects.filter(record_id=record_id, index=index).values(
            "id" ,"user__username", "body", "rating", "created_at"
        )

        return Response(list(comments), status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        comment_id = request.data.get("comment_id")
        if not comment_id:
            return Response({"error": "Missing comment_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(id=comment_id, user=user) 
            comment.delete()
            return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
