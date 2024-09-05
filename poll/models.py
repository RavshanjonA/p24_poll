from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Poll(models.Model):
    question = models.TextField()
    author = models.ForeignKey(User, CASCADE, "polls")
    published = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    answer = models.TextField()
    poll = models.ForeignKey(Poll, CASCADE, "choices")


class Vote(models.Model):
    poll = models.ForeignKey(Poll, CASCADE, "votes")
    choice = models.ForeignKey(Choice, CASCADE, "votes")
    voted_by = models.ForeignKey(User, CASCADE, "votes")
    voted_at = models.DateTimeField(auto_now=True)
