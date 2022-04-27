from .models import User, Subcription, Session, Ticket
from rest_framework import serializers


class AdminUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'user_type')
        
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'user_type')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'password')
        
class LoginSerializer(serializers.ModelSerializer):
   password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    
   class Meta:
        model = User
        fields = ('username', 'password')
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'user_type')
        
class NewsLetter(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    body = serializers.CharField()
    
    class Meta:
        model = User
        fields = ('title', 'body')
        
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcription
        fields = ('subscription_type', )
        
class SubscriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcription
        fields = "__all__"
        
class SessionSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Session
        fields = ['users','title', 'description', 'session_date', 'is_done']
        
class TicketSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Ticket
        fields = ['users', 'ticket_title', 'ticket_description', 'is_resolved']