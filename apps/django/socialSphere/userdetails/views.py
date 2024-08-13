# views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import SS_User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password,make_password
from .models import SS_User
from .serializers import UserSerializer
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from django.utils import timezone
from datetime import timedelta


class UserViewSet(viewsets.ModelViewSet):
    queryset = SS_User.objects.all()  
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Custom logic for user signup if needed
        return super().create(request, *args, **kwargs)
    
    
class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()  
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            return FriendRequest.objects.filter(to_user=user)
        return FriendRequest.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=user, created_at__gte=one_minute_ago).count()

        if recent_requests >= 3:
            return Response({'error': 'You cannot send more than 3 friend requests within a minute.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(from_user=user)
        

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email').lower()
    password = request.data.get('password')
    
    user = SS_User.objects.filter(email=email).first()
    
    if user and check_password(password, user.password):
        return Response({"msg":UserSerializer(user).data, "status":True})
    
    return Response({'error': 'Invalid credentials', "status":False})


@api_view(['POST'])
def user_signup(request):
    
    user_name = request.data.get('user_name')
    category = request.data.get('category', 1 )
    active_status = request.data.get('active_status', True)  
    login_time = request.data.get('login_time', None)  
    email = request.data.get('email').lower()  
    password = request.data.get('password')
    
    if SS_User.objects.filter(email=email).exists():
        return Response({'error': 'Email is already registered.', "status":"BAD_REQUEST"})
    
    hashed_password = make_password(password)
    
    
    user = SS_User.objects.create(
        user_name=user_name,
        category=category,
        active_status=active_status,
        login_time=login_time,
        email=email,
        password=hashed_password
    )
    
 
    serializer = UserSerializer(user)
    return Response({"msg":serializer.data, "status":True})


@api_view(['POST'])
def send_friend_request(request):
    from_user_id = request.data.get('from_user_id')
    to_user_id = request.data.get('to_user_id')

    if not from_user_id or not to_user_id:
        return Response({'error': 'Both from_user_id and to_user_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from_user = SS_User.objects.get(id=from_user_id)
        to_user = SS_User.objects.get(id=to_user_id)
    except SS_User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if a request already exists
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check for the rate limit
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    recent_requests = FriendRequest.objects.filter(from_user=from_user, created_at__gte=one_minute_ago).count()
    if recent_requests >= 3:
        return Response({'error': 'You cannot send more than 3 friend requests within a minute.'}, status=status.HTTP_400_BAD_REQUEST)

    friend_request = FriendRequest.objects.create(
        from_user=from_user,
        to_user=to_user,
        status='request sent' 
    )

    return Response({'message': 'Friend request sent.', 'data': {'from_user': from_user_id, 'to_user': to_user_id, 'status': friend_request.status}}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_friend_request(request):
    request_id = request.data.get('request_id')
    # to_user_id = request.data.get('to_user_id')

    try:
        friend_request = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request not found or you are not the recipient.'}, status=status.HTTP_404_NOT_FOUND)
    if friend_request.status == "request sent":
        friend_request.accept()
        return Response({'message': 'Friend request accepted and added to friends list.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': f'friend requet already got {friend_request.status}', 'status':status.HTTP_200_OK})

@api_view(['GET'])
def list_pending_friend_requests(request):
    user = request.data.get('user')
    pending_requests = FriendRequest.objects.filter(to_user=user, status='request sent')
    
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response({'pending_requests': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reject_friend_request(request):
    request_id = request.data.get('request_id')
    # to_user_ = request.data.get('to_user')
    try:
        friend_request = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request not found or you are not the recipient.'}, status=status.HTTP_404_NOT_FOUND)
    
    if friend_request.status == "request sent":
        friend_request.status = 'rejected'
        friend_request.save()
        
        return Response({'message': 'Friend request rejected.', 'status':status.HTTP_200_OK})
    else:
        return Response({'message': f'friend requet already got {friend_request.status}', 'status':status.HTTP_200_OK})

@api_view(['GET'])
def list_friends(request):
    user_id = request.data.get('user_id')

    try:
        user = SS_User.objects.get(id=user_id)
    except SS_User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    friends_list = user.friends_list.friends.all()
    serializer = UserSerializer(friends_list, many=True)
    
    return Response({
        'msg': serializer.data, 
        'status': status.HTTP_200_OK
    })

