# urls.py

from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friendrequests', FriendRequestViewSet)

urlpatterns = [
    path('signup', user_signup, name='user_signup'),
    path('login', user_login, name='user_login'),
    path('friend_request_send', send_friend_request, name='send_friend_request'),
    path('friend_request_accept', accept_friend_request, name='accept_friend_request'),
    path('friend_request_reject', reject_friend_request, name='reject_friend_request'),
    path('friends/', list_friends, name='list_friends'),
    path('pending_friend_requests', list_pending_friend_requests, name='list_pending_friend_requests'),  # New endpoint

]
