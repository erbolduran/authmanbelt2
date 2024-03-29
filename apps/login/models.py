# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from ..wall.models import *


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check name fields for letter characters            
        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")


        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                email=post_data['email'],
                password=hashed
            )
            print new_user
            return new_user
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    favs = models.ManyToManyField(
        "User",
        symmetrical = False,
        through='Favorite',
        through_fields=('from_liker', 'to_liked')
    )

    objects = UserManager()
    def __unicode__(self):
        return 'first_name: {}, last_name: {}, email: {}, password: {}, favs: {}, id: {}'.format(self.first_name, self.last_name, self.email, self.password, self.favs, self.id)

class Favorite(models.Model):
    from_liker = models.ForeignKey(User, related_name = 'from_fav')
    to_liked   = models.ForeignKey('wall.Message', related_name = 'to_fav')
    favmessage = models.BooleanField(False)

    def __unicode__(self):
        return 'from_liker: {}, to_liked: {}, favmessage: {}, id: {}'.format(self.from_liker, self.to_liked, self.favmessage, self.id)


