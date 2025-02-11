from rest_framework.response import Response
from rest_framework import viewsets , status
from .models import User , Message , SubscriptionPlan , Task
from django.utils.timezone import now
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import UserSerializer , AllUsers , TaskSerializer , MessageSerializer


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Use the serializer to create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Retrieve tokens from the serializer's context
        tokens = serializer.context.get('tokens')

        # Build the response
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED, headers=headers)


class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all() 
    serializer_class = AllUsers

class SendMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipient_id = request.data.get('recipient')
        body = request.data.get('body')

        if recipient_id == request.user.id :
            return Response(
                {'error' : 'You can not message to yourself !'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Recipient does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = Message.objects.create(
            recipient=recipient,
            body=body
        )
        return Response(
            {
                'id': message.id,
                'recipient': recipient.username,
                'body': message.body,
                'read' : message.read ,
                'created_at': message.created_at
            },
            status=status.HTTP_201_CREATED
        )

class GetUserMessagesView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user
        messages = Message.objects.filter(recipient=user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
class ChangeSubscriptionPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        plan_name = request.data.get('plan')

        try:
            plan = SubscriptionPlan.objects.get(name=plan_name)
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Invalid plan name'}, status=status.HTTP_400_BAD_REQUEST)

        user_subscription = user.subscription
        user_subscription.plan = plan
        user_subscription.end_date = now() + plan.duration
        user_subscription.save()

        return Response({
            'message': f'Successfully changed to {plan.name.capitalize()} plan',
            'plan': plan.name,
            'end_date': user_subscription.end_date
        }, status=status.HTTP_200_OK)
    

class TaskViewList(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

