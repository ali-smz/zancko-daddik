from django.db import models
from django.core.validators import MinLengthValidator , MinValueValidator , MaxValueValidator

# Create your models here.
class RealPerson(models.Model):
    username = models.CharField(max_length=50 , unique=True)
    password = models.CharField(max_length=50 , validators=[MinLengthValidator(8)])
    name = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    national_code = models.CharField(max_length=10 , unique=True)
    phoneNumber = models.CharField(max_length=11)
    address = models.CharField(max_length=50)
    workNumber = models.CharField(max_length=11 , blank=True)
    role  = models.CharField(max_length=20 , blank=True)
    stars = models.IntegerField(validators=[MinValueValidator(0) , MaxValueValidator(5)] , default=0)
    isPremium = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)  
    updatedAt = models.DateTimeField(auto_now=True)    


    def __str__(self):
        return f'{self.name} {self.lastName} | {self.national_code}'
    


class LegalPerson(models.Model):
    username = models.CharField(max_length=50 , unique=True)
    password = models.CharField(max_length=50 , validators=[MinLengthValidator(8)])
    companyName = models.CharField(max_length=50)
    companyNationalId = models.CharField(max_length=11 , unique=True)
    address = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=11)
    document = models.FileField(upload_to='uploads/pdfs')
    officialNewspaper = models.FileField(upload_to='uploads/pdfs')
    companyWebsite = models.CharField(max_length=100)
    companyEmail = models.EmailField(max_length=254)
    connectorName = models.CharField(max_length=50)
    connectorLastname = models.CharField(max_length=50)
    connectorNationalCode = models.CharField(max_length=10)
    connectorPhoneNumber = models.CharField(max_length=11)
    connectorRole  = models.CharField(max_length=20 , blank=True)
    introductionLetter = models.FileField(upload_to='uploads/pdfs')
    stars = models.IntegerField(validators=[MinValueValidator(0) , MaxValueValidator(5)] , default=0)
    isPremium = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)  
    updatedAt = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f'{self.companyName} | {self.connectorName} {self.connectorLastname} | {self.connectorNationalCode}'