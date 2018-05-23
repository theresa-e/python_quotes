from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class ErrorManager(models.Manager):
    def basic_validator(self, requestPOST):
        errors = {}
        user_list = User.objects.filter(email=requestPOST['email'])
        if len(requestPOST['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters long."
        if len(requestPOST['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters long."
        if len(requestPOST['email']) < 2:
            errors['email'] = "Email required for registration."
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['email_format'] = "Please enter a valid email."
        if len(requestPOST['password']) < 8:
            errors['password_len'] = "Password must be at least 8 characters long."
        if requestPOST['password'] != requestPOST['confirm_password']:
            errors['password_match'] = "Please confirm password before registering, they do not match."
        if len(user_list) > 0:
            errors['existing_user'] = "That email is already associated with an account."
        if not len(errors):
            hash = bcrypt.hashpw(requestPOST['password'].encode(), bcrypt.gensalt())
            print(hash)
            user = User.objects.create(first_name=requestPOST['first_name'], last_name=requestPOST['last_name'], email=requestPOST['email'], pw_hash=hash)
            user.save()
        return errors

    def login_validator(self, requestPOST):
        errors = {}
        user_list = User.objects.filter(email=requestPOST['login_email'])
        if not EMAIL_REGEX.match(requestPOST['login_email']):
            errors['login_format'] = "Please enter a valid email."
        if len(requestPOST['login_email']) < 1:
            errors['login_email'] = "Login email cannot be blank."
        if len(user_list) < 1:
            errors['email_error'] = "This email is not associated with an account."
        if len(user_list) > 0:
            user = User.objects.get(email=requestPOST['login_email'])
            hash1 = bcrypt.hashpw('test'.encode(), bcrypt.gensalt())
            if not bcrypt.checkpw(requestPOST['login_password'].encode(), user.pw_hash.encode()):
                errors['pw_error'] = "You could not be logged in."
            else:
                print('-'*30+'> ', 'Password is correct!')
                print('-'*30+'> ', 'User logged in successfully. ')
        return errors

    def update_info_validator(self, requestPOST):
        errors = {}
        user = User.objects.get(id=requestPOST['userid'])
        email_check = User.objects.filter(email=requestPOST['email'])
        if len(requestPOST['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters long."
        if len(requestPOST['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters long."
        if len(requestPOST['email']) < 2:
            errors['email'] = "Email required for registration."
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['email_format'] = "Please enter a valid email."
        if len(email_check) > 0:
            if requestPOST['email'] == user.email:
                pass 
                # User didn't change email
            else:
                errors['email_exists'] = "The email you entered is already in use. Please enter a different one."
        return errors
        

    def quote_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['quote']) < 10:
            errors['quote_len'] = "Provide the entire quote."
        if len(requestPOST['author']) < 3:
            errors['author_len'] = "Enter the author's entire name."
        if not len(errors):
            user = User.objects.get(id=requestPOST['userid'])
            new_quote = Quote.objects.create(quote=requestPOST['quote'], author=requestPOST['author'], uploaded_by=user)
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    pw_hash = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ErrorManager()
    def __repr__(self):
        return "<User object: first_name: {}, last_name: {}, email: {}, pw_hash: {}>".format(self.first_name, self.last_name, self.email, self.pw_hash)

class Quote(models.Model):
    quote = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name="liked_quotes")
    uploaded_by = models.ForeignKey(User, related_name="uploaded_quotes")
    objects = ErrorManager()
    def __repr__(self):
        return "<Quote object: quote: {}, author: {}, liked_by: {}, uploaded_by: {}>".format(self.quote, self.author, self.liked_by, self.uploaded_by)
