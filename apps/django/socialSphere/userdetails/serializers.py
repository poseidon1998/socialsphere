from rest_framework import serializers
from .models import SS_User, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SS_User
        fields = ['id', 'user_name', 'category', 'active_status', 'login_time', 'email']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField()  # Display related user's email
    to_user = serializers.StringRelatedField()      # Display related user's email

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
