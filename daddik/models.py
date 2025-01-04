import random
import string
from django.db import models
from django.core.validators import MinLengthValidator , MinValueValidator , MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class User(AbstractBaseUser):
    STATUS_CHOICES = [
        ('real', 'Real'),
        ('legal', 'Legal'),
        ('unknown', 'Unknown'),
    ]

    lable = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown')
    username = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=50, validators=[MinLengthValidator(8)])
    profilePicture = models.FileField(upload_to='uploads/images', blank=True)
    name = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50, blank=True)
    job = models.CharField(max_length=50, blank=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True)
    workNumber = models.CharField(max_length=11, null=True, blank=True)
    role = models.CharField(max_length=20, blank=True)
    companyName = models.CharField(max_length=50, blank=True)
    companyNationalId = models.CharField(max_length=11, unique=True, null=True, blank=True)
    document = models.FileField(upload_to='uploads/pdfs', blank=True)
    officialNewspaper = models.FileField(upload_to='uploads/pdfs', blank=True)
    companyWebsite = models.CharField(max_length=100, blank=True)
    companyEmail = models.EmailField(max_length=254, blank=True)
    connectorName = models.CharField(max_length=50, blank=True)
    connectorLastname = models.CharField(max_length=50, blank=True)
    connectorNationalCode = models.CharField(max_length=10, blank=True)
    connectorPhoneNumber = models.CharField(max_length=11, blank=True)
    connectorRole = models.CharField(max_length=20, blank=True)
    introductionLetter = models.FileField(upload_to='uploads/pdfs', blank=True)
    searchs = models.IntegerField(validators=[MinValueValidator(0) , MaxValueValidator(7)] , default=0)
    billsNumber = models.IntegerField(validators=[MinValueValidator(0) , MaxValueValidator(3)] , default=0)
    stars = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='referrals', null=True, blank=True
    )
    referral_count = models.IntegerField(default=0)
    isPremium = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    groups = None
    user_permissions = None
    is_superuser = None
    last_login = None

    objects = UserManager()

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = [] 

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_referral_code(length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def __str__(self):
        return f'{self.username} | {self.lable}'



class Message(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages'
    )
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message to {self.recipient.username} at {self.created_at}'