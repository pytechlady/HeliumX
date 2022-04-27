from itertools import permutations
from webbrowser import get
from requests import request
from rest_framework.response import Response
from django.shortcuts import render
from .models import Subcription, User, Session, Ticket
from rest_framework import generics, status, permissions
from .serializers import AdminUserSerializer, UserListSerializer, LoginSerializer, UserUpdateSerializer, NewsLetter, UserSerializer, SubscriptionSerializer, SubscriptionListSerializer, SessionSerializer, TicketSerializer
from .permissions import IsCeo, IsCommunutyManager, IsAccountantPermissions, IsITSupportPermissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .utils import Util


class RegisterAdminsClass(generics.GenericAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = (IsCeo,)
    
    """Endpoint to register staffs only accessible by CEO"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            first_name =serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user_type = serializer.validated_data['user_type']
            try:    
                user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
                if user_type == 'Community Manager':
                    user.is_community_manager = True
                elif user_type == 'Accountant':
                    user.is_accountant = True
                elif user_type == 'IT Support':
                    user.is_IT_support = True
                elif user_type == 'Admin':
                    user.is_admin = True
                user.save()
                return Response({"success": f"{username} successfully created"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateAdminClass(generics.GenericAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = (IsCeo,)
    queryset = ''
    
    """Endpoint to check if a user or staff exists only accessible by CEO"""
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)    
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    """Endpoint to get a user or staff only accessible by CEO"""
    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = AdminUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """Endpoint to update users and staffs only accessible by CEO"""
    def patch(self, request, pk):
        user = self.get_user(pk)
        serializer = AdminUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """"Endpoint to delete a user or staff only accessible by CEO"""
    def delete(self, request, pk):
        user = self.get_user(pk)
        email = user.email
        user.delete()
        return Response({"success": f"User with {email} successfully deleted"}, status=status.HTTP_200_OK)
    
    
class RegisterUsers(generics.GenericAPIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
    """Endpoint to register other users who are not staffs"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            first_name =serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            try:    
                user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
                user.basic_user = True
                user.save()
                return Response({"success": f"{username} successfully created"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserByCommunityManager(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated, IsCommunutyManager]
    serializer_class = UserSerializer
    queryset = ''
    
    """Endpoint to check if a user exists only accessible by Community Manager"""
    def get_user(self, pk):
        try:
            user =User.objects.get(pk=pk)   
            return user
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    """Endpoint to get a user only accessible by Community Manager"""
    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    """Endpoint to update a user only accessible by Community Manager"""   
    def patch(self, request, pk):
        user = self.get_user(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                if user.is_CEO:
                    return Response({"error": "You are not allowed to update this user"}, status=status.HTTP_400_BAD_REQUEST)
                if user.is_admin:
                    return Response({"error": "You are not allowed to update this user"}, status=status.HTTP_400_BAD_REQUEST)
                if user.is_IT_support:
                    return Response({"error": "You are not allowed to update this user"}, status=status.HTTP_400_BAD_REQUEST)
                if user.is_community_manager and user.id != request.user.id:
                    return Response({"error": "You are not allowed to update this user"}, status=status.HTTP_400_BAD_REQUEST)
                if user.is_accountant:
                    return Response({"error": "You are not allowed to update this user"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response({"success": f"{user.username} successfully updated"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        

"""Endpoint to view all users details accessible by CEO or Community Manager"""
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsCommunutyManager | IsCeo]
    filterset_fields = ['is_community_manager', 'is_accountant', 'is_IT_support', 'is_admin']
    
    
class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permissions_classes = [permissions.AllowAny]
    
    """Endpoint to login a user"""
    def post (self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        try:
            user = User.objects.get(username=username)
            if password == user.password:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(data={'token': token.key,'username': user.username}, status=status.HTTP_200_OK)
            if not user:
                return Response(data={'invalid_credentials': 'Ensure both username and password are correct and you have verified your account'}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as error:
            return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)


class SendNewsLetter(generics.GenericAPIView):
    permissions_classes = [IsCommunutyManager]
    serializer_class = NewsLetter
    
    """Endpoint to send a newsletter to all users only accessible by Community Manager"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        get_all_users_emails = User.objects.all().values_list('email', flat=True)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            body = serializer.validated_data['body']
            try:
                for email in get_all_users_emails:
                    email_body = f"{title} \n\n {body}"
                    data = data = {'email_body': email_body, 'to_email': email, 'email_subject': title}
                    Util.send_email(data)
                return Response({"success": f"{title} successfully sent"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateSubscription(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer
    
    """Endpoint for users to create a subscription"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = request.user   
        print(user)
        if serializer.is_valid():
            subscription_type = serializer.validated_data['subscription_type']
            try:
                Subcription.objects.create(subscription_type=subscription_type, user=user)
                return Response({"success": f"{user} successfully subscribed"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UpdateSubscription(generics.GenericAPIView):
    permissions_classes = [IsAccountantPermissions]
    serializer_class = SubscriptionListSerializer
    queryset = ''
    
    """Endpoint to check if a user exists only accessible by Accountant"""
    def get_user(self, pk):
        try:
            user =User.objects.get(pk=pk)   
            return user
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
     
    """Endpoint to get a user if he is a subscriber only accessible by Accountant"""   
    def get(self, request, pk):
        user = self.get_user(pk)
        get_subscription = Subcription.objects.filter(user=user).first()
        serializer = SubscriptionListSerializer(get_subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """Endpoint to update a user subscription only accessible by Accountant"""
    def patch(self, request, pk): 
        user = self.get_user(pk)
        get_subscription = Subcription.objects.filter(user=user).first()
        serializer = SubscriptionListSerializer(get_subscription, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"success": f"{get_subscription} successfully updated"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)


class CreateSession(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated, IsITSupportPermissions]
    serializer_class = SessionSerializer
    
    """Endpoint to create a session"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            users = serializer.validated_data['users']
            title = serializer.validated_data['title']
            description = serializer.validated_data['description']
            session_date = serializer.validated_data['session_date']
            is_done = serializer.validated_data['is_done']
            try:
                Session.objects.create(title=title, session_date=session_date, description=description, user=users[0], is_done=is_done)
                return Response({"success": f"A session has been created for {users}"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateSession(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated, IsITSupportPermissions]
    serializer_class = SessionSerializer
    queryset = ''
    
    """Endpoint to get all sessions"""
    def get(self, request):
        get_sessions = Session.objects.all()
        serializer = SessionSerializer(get_sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """Endpoint to update session progress"""
    def patch(self, request, pk):
        get_session = Session.objects.get(pk=pk)
        serializer = SessionSerializer(get_session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": f"{get_session} successfully updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CreateTickets(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated, IsITSupportPermissions]
    serializer_class = TicketSerializer
    
    """Endpoint to create a ticket"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            users = serializer.validated_data['users']
            ticket_title = serializer.validated_data['ticket_title']
            ticket_description = serializer.validated_data['ticket_description']
            is_resolved = serializer.validated_data['is_resolved']
            try:
                Ticket.objects.create(ticket_title=ticket_title, ticket_description=ticket_description, is_resolved=is_resolved, user=users[0])
                return Response({"success": f"A ticket has been created for {users}"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UpdateTickets(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated, IsITSupportPermissions]
    serializer_class = TicketSerializer
    queryset = ''
    
    """Endpoint to get all tickets"""
    def get(self, request):
        get_tickets = Ticket.objects.all()
        serializer = TicketSerializer(get_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """Endpoint to update ticket progress"""
    def patch(self, request, pk):
        get_ticket = Ticket.objects.get(pk=pk)
        serializer = TicketSerializer(get_ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": f"{get_ticket} successfully resolved"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD)

   
                
