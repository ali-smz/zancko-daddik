from rest_framework.response import Response
from rest_framework import viewsets , status
from .models import User , Message , SubscriptionPlan , Task , UserSubscription , SubscriptionHistory
from django.utils.timezone import now
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import UserSerializer  , TaskSerializer , MessageSerializer
from datetime import timedelta
from django.utils.crypto import get_random_string           
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

        tokens = serializer.context.get('tokens')

        # Build the response
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED, headers=headers)
    

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        old_label = user.lable
        serializer = self.get_serializer(user, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        new_label = updated_user.lable

        if old_label != new_label and new_label == "legal" :
            self.assign_legal_user_tasks(updated_user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def assign_legal_user_tasks(self , user) : 
        task_to_add = [
            {
                "title": "Submit Company Documents",
                "description": "Upload all required company documents to complete verification.",
                "deadline": now() + timedelta(days=7)
            },
            {
                "title": "Submit Company Documents",
                "description": "Upload all required company documents to complete verification.",
                "deadline": now() + timedelta(days=7)
            },
            {
                "title": "Submit Company Documents",
                "description": "Upload all required company documents to complete verification.",
                "deadline": now() + timedelta(days=7)
            }
        ]

        for task in task_to_add:
            Task.objects.create(user=user , **task)

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
        organ = request.data.get('organ') if request.data.get('organ') else "all"

        try:
            plan = SubscriptionPlan.objects.get(name=plan_name)
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Invalid plan name'}, status=status.HTTP_400_BAD_REQUEST)

        user_subscription = UserSubscription.objects.filter(user=user).order_by('-end_date').first()

        if not user_subscription:
            return Response({'error': 'No active subscription found'}, status=status.HTTP_400_BAD_REQUEST)

        old_plan = user_subscription.plan 

        user_subscription.plan = plan
        user_subscription.end_date = now() + plan.duration
        user_subscription.organ = organ
        user_subscription.save()

        transaction_reference = get_random_string(length=16)  # Generate a unique reference for the transaction
        SubscriptionHistory.objects.create(
            user=user,
            old_plan=old_plan,
            new_plan=plan,
            transaction_reference=transaction_reference
        )

        return Response({
            'message': f'Successfully changed to {plan.name.capitalize()} plan',
            'plan': plan.name,
            'organ' : user_subscription.organ ,
            'end_date': user_subscription.end_date
        }, status=status.HTTP_200_OK)


class SubscriptionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        history = SubscriptionHistory.objects.filter(user=user).order_by('-change_date')
        
        history_data = [
            {
                'old_plan': history_item.old_plan.name,
                'new_plan': history_item.new_plan.name,
                'change_date': history_item.change_date,
                'transaction_reference': history_item.transaction_reference
            }
            for history_item in history
        ]

        return Response({'history': history_data}, status=status.HTTP_200_OK)


class TaskViewList(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

