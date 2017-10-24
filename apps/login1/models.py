from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import md5
import os, binascii
#import bcrypt

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = []
        if len(postData['first_name']) < 2:
            errors.append('Names need to be at least 2 characters')
        if len(postData['last_name']) < 2:
            errors.append('Names need to be at least 2 characters')
        if not NAME_REGEX.match(postData['first_name']):
            errors.append('First name must only contain alphabet')
        if not NAME_REGEX.match(postData['last_name']):
            errors.append('Last name must only contain alphabet')
        if len(postData['password']) < 8:
            errors.append('Password needs to be at least 8 characters')
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append('email already in use')
        if postData['password'] != postData['confirm_password']:
            errors.append('Passwords do not match')

        if len(errors) == 0:
            salt = binascii.b2a_hex(os.urandom(15))
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], salt=salt, password=hashed_pw)
        return errors

    def validate_log(self, postData):
        errors = []
        if User.objects.filter(email=postData['email']):
            salt = User.objects.get(email=postData['email']).salt
            hashed_pw = md5.new(salt + postData['password']).hexdigest()
            if User.objects.get(email=postData['email']).password != hashed_pw:
                errors.append('Incorrect password')
        else:
            errors.append('Email has not been registered')
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.EmailField(unique = True)
    salt = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return str(self.id) + self.first_name + self.last_name + self.email + self.salt + self.password