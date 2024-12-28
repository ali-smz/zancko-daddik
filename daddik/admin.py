from django.contrib import admin
from .models import RealPerson , LegalPerson
# Register your models here.

admin.site.register(RealPerson)
admin.site.register(LegalPerson)