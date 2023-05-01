from django.db import models
# from django.contrib.auth.models import Permission
from django.contrib.auth.models import User


# Create your models here.
class student(models.Model):
    #id = models.IntegerField()
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    city = models.CharField(max_length=15)
    phonenumber = models.CharField(max_length=15,null=True)

    def __str__(self):
        return self.firstname

class User(models.Model):
    user_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class PermissionModel(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    permission_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table='permission_mapping'