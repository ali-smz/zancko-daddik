from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
# Create your views here.
API_ROUTE = 'https://api.legaldadik.ir/v1/chat'


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if not message :
                return JsonResponse({'error': 'Message is required'}, status=400)
            response = requests.post(API_ROUTE, json={'message': message})
            return JsonResponse({'message': response.json()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

