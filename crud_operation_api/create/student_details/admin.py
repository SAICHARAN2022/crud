from django.contrib import admin
from .models import student
# Register your models here.
admin.site.register(student)

class studentadmin(admin.ModelAdmin):
    list_display = ['firstname','lastname','city','phonenumber']