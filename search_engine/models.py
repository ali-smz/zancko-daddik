# import random
# import string
# from django.db import models
# from django.core.validators import MinLengthValidator , MinValueValidator , MaxValueValidator
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils.timezone import now
# from django.conf import settings



# class Message(models.Model):
#     recipient = models.CharField(max_length=500)
#     body = models.TextField()
#     read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Message to {self.recipient.username} at {self.created_at}'