# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name_error'] = "First name and Last name must be 2 or more characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not Valid"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['pass_length'] = "Password must be 8 or more characters"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Password must match"
        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already taken"
        return errors
    def login(self, postData):
        
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) > 0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = { "user": user_to_check}
                return user
                errors['error'] = "Email/Password invalid"
            else:
                errors = {"error": "Login Invalid"}
                return errors
        else:
            errors = {"error": "Login Invalid"}
            return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()