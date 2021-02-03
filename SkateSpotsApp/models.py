from django.db import models
# from django.core.validators import validate_email
from django.contrib import messages
# from django.contrib.messages import get_messages
import re
from datetime import date, datetime, timedelta
import timeago
# import pytz
from django.contrib.sites.models import Site
from PIL import Image
from django_s3_storage.storage import S3Storage

storage = S3Storage(aws_s3_bucket_name='django-skate-spots')


class UserManager(models.Manager):
    def is_reg_valid(self, request):

        NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
        if not NAME_REGEX.match(request.POST['first_name']):
            messages.error(request, "Please enter your First Name")
        if not NAME_REGEX.match(request.POST['last_name']):
            messages.error(request, "Please enter your Last Name")

        if len(request.POST['first_name']) < 2:
            messages.error(
                request, "First Name should be at least 2 characters")

        if len(request.POST['last_name']) < 2:
            messages.error(
                request, "Last Name should be at least 2 characters")

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, "Invalid email")

        if len(request.POST['password']) < 8:
            messages.error(request, "Password should be at least 8 characters")

        if request.POST['password'] != request.POST['confirm_password']:
            messages.error(request, "Passwords do not match")

        if (request.POST['birthday']) == '':
            messages.error(request, "Must enter a birthday")

        else:
            birthday = datetime.strptime(request.POST['birthday'], "%Y-%m-%d")

            today = date.today()
            now = datetime.now()
            age = (today.year - birthday.year -
                   ((today.month, today.day) <
                    (birthday.month, birthday.day)))

            if birthday > datetime.today():
                messages.error(request, "Birthday can not be a future date")

            if age < 13:
                messages.error(request, "Must be at least 13 to register")

        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday = models.DateField()
    photo = models.ImageField(
        upload_to="images/", null=True, blank=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User object: id: {self.id}, title: {self.email}>"

    def __str__(self):
        return self.email


class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="messages")
    subject = models.CharField(max_length=100, default="Title")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_delete(self):
        time_delta = timedelta(minutes=30)
        timer = self.created_at.replace(tzinfo=None)
        now = datetime.now()
        timeago.format(timer, now)

        if now - timer < time_delta:
            return True
        else:
            return False

        def __repr__(self):
            return f"<Message object: id: {self.id}, title: {self.user}>"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_comments")
    message = models.ForeignKey(
        Message, on_delete=models.PROTECT, related_name="message_comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Comment object: id: {self.id}, title: {self.comment}>"


class Marker(models.Model):
    name = models.CharField(max_length=60)
    photo = models.ImageField(storage=storage, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True, default=None)
    long = models.FloatField(null=True, blank=True, default=None)
    kind = models.CharField(max_length=60)
    desc = models.CharField(max_length=120)
    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Marker object: id: {self.id}, photo: {self.photo}, title: {self.name}, desc: {self.desc}>"

    def __str__(self):
        return self.name
        