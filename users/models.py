from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    basic_user =models.BooleanField(default=False)
    is_CEO = models.BooleanField(default=False)
    is_community_manager = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)
    is_IT_support = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    roles = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    

class Role(models.Model):
    role = models.CharField(max_length=50)
    
    def __str__(self):
        return self.role
    

class Subcription(models.Model):
    SUBSCRIPTION_TYPE_CHOICES =[
        ('BASIC', 'BASIC'),
        ('PREMIUM', 'PREMIUM'),
    ]
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    booking_date = models.DateTimeField(auto_now_add=True)
    session_date = models.DateField()
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_title = models.CharField(max_length=100)
    ticket_description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ticket_title