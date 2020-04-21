from __future__ import unicode_literals
from django.db import models 
import bcrypt
import re 
import datetime
 
# create your models here 
# Field Types Link: https://docs.djangoproject.com/en/1.11/ref/models/fields/#field-types 


class UserManager(models.Manager):
    # Basic Validation and Duplicate Detection
    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if len(postData['email']) < 7:
            errors['email'] = "Email must be at least 7 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_regex'] = "Email must be in the correct format ex: email@provider.com"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters "
        if not postData['password_confirm'] == postData['password']:
            errors['password_confirm'] = "Password does not match Confirm Password"
        if len(User.objects.filter(email=postData['email'])):
            errors['duplicate'] = "Email already exists"
        if postData['dob'] > str(datetime.date.today()):
            errors['dob'] = "Your birthday is set in the future... Are you a time traveller?"
        
        # Create a date object to compare with postData['dob']
        today = datetime.datetime.now()
        requiredAge = 13
        age_requirement_date = "" + str(today.year - requiredAge) + "-" + str(today.month) + '-' + str(today.day)
        if str(postData['too_young']) > age_requirement_date:
            errors['too_young'] = "You must be at least " + str(requiredAge) + " years old to use this site"



        return errors

    def login_validator(self, postData):
        # Validates Login Info
        login_errors = {}

        if postData['login_email']:
            thisUser = User.objects.filter(email=postData['login_email']).first()
            if thisUser:
                if not bcrypt.checkpw(postData['login_password'].encode(), thisUser.pw_hash.encode()):
                    login_errors['login_password'] = "Invalid Credentials"
            else:
                login_errors['login_email'] = "Email not in our database"
        else:
            login_errors['login_email'] = "Please enter a valid email"

        return login_errors




class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()




