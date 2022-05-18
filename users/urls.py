from django.urls import path
from .views import *


urlpatterns = [
    path('register', RegisterAdminsClass.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('users', UserList.as_view(), name='users'),
    path('users/<int:pk>', UpdateAdminClass.as_view(), name='user-detail'),
    path('newsletter', SendNewsLetter.as_view(), name='newsletter'),
    path('sign-up', RegisterUsers.as_view(), name='sign-up'),
    path('user/<int:pk>', UpdateUserByCommunityManager.as_view(), name='user'),
    path('subscribe', CreateSubscription.as_view(), name='subscribe'),
    path('user/<int:pk>/subscribe', UpdateSubscription.as_view(), name='subscribe'),
    path('session', CreateSession.as_view(), name='session'),
    path('session/<int:pk>', UpdateSession.as_view(), name='session'),
    path('ticket', CreateTickets.as_view(), name='ticket'),
    path('ticket/<int:pk>', UpdateTickets.as_view(), name='ticket'),
    path('role', CreateRole.as_view(), name='role'),
]
