from __future__ import unicode_literals
from django.db import models
import re
# Create your models here.
from datetime import date , datetime

class UserManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 1: # check if name has a value
            errors["first_name"] = "First name must be present"
        if len(postData['last_name']) < 1: # check if name has a value
            errors["last_name"] = "Last name must be present"
        if len(postData['email']) < 1: # check if email has value
            errors["email"] = "Email must be present"
        elif not EMAIL_REGEX.match(postData['email']):   # check if email is proper format based on regex       
            errors['email'] = "Invalid email address!"
        else:
            email_found = False
            for user in Users.objects.all():
                if user.email == postData['email']:
                    email_found = True
            if email_found == True:
                errors['email'] = "Email address already registered"
        if len(postData['password']) < 8: # check if password has at least 8 characters
            errors["password"] = "Password should be at least 8 characters"

        if postData['verf_password'] != postData['password']: # check if password matches 
            errors['verf_password'] = 'Passwords does not match'
        return errors

class TripManager(models.Manager):

    def basic_validator(self,postData):
        today = str(date.today())
        errors = {}
        if len(postData['destination']) == 0:
            errors["destination"] = "Destination must be present"
        elif len(postData['destination']) < 3: # check if name has a value
            errors["destination"] = "Destination must have at least 3 characters"
        if len(postData['plan']) == 0:
            errors["plan"] = "Plan must be present"
        elif len(postData['plan']) < 3: # check if name has a value
            errors["plan"] = "Plan have at least 3 characters"
        if len(postData['start_date']) == 0:
            errors["start_date"] = "Start date must be present"
        elif postData['start_date'] < today: # check if capacity is greater than 0
            errors["start_date"] = "Start date cannot be in the past"
        if len(postData['end_date']) == 0:
            errors["end_date"] = "End date must be present"
        elif postData['end_date'] < postData['start_date']: # check if capacity is greater than 0
            errors["end_date"] = "End date cannot earlier than start_date"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

class Trips(models.Model):
    destination = models.CharField(max_length = 255)
    plan = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date =  models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    created_by =  models.ForeignKey(Users, related_name="trips_created", on_delete = models.CASCADE)
    user_participants =  models.ManyToManyField(Users, related_name="trips_joined")
    objects = TripManager()