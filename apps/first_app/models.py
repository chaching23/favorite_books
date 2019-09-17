
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class manager(models.Manager):
 
    def register_user(self, form):
        hashed = bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt())
        new_guy = self.create(first_name=form["first_name"], last_name=form["last_name"], email=form["email"], password=hashed)
        return new_guy.id


    def validate_registration(self, form):
        errors = []
        if len(form['first_name']) <3:
            errors.append("First name should be at least 2 characters")

        if len(form['last_name']) <3:
            errors.append("Last name should be at least 2 characters")

        if not EMAIL_REGEX.match(form['email']):   
            errors.append("Not a valid email")
        
        if len(form['password']) < 9:
            errors.append("Password must be atleast 8 characters long")

        if len(form['cpassword']) < 9:
            errors.append("Password must be atleast 8 characters long")
        
        if form['password']!= form['cpassword']:
            errors.append("Passwords do not match")


        result = self.filter(email=form["email"])
        if result:
            errors.append("Email already in use")
        return errors






class data(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    cpassword = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = manager()

class book(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.ManyToManyField(data,related_name="books")

