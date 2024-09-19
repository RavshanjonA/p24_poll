from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import CASCADE, UniqueConstraint, FileField

from account.models import Account


class Poll(models.Model):
    question = models.TextField()
    author = models.ForeignKey(Account, CASCADE, "polls")
    published = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    audio = FileField(upload_to="audios/", null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=["mp3", "ogg"])])
    poll = models.ForeignKey(Poll, CASCADE, "choices")


class Vote(models.Model):
    choice = models.ForeignKey(Choice, CASCADE, "votes")
    voted_by = models.ForeignKey(Account, CASCADE, "votes")
    voted_at = models.DateTimeField(auto_now=True)
    poll = models.ForeignKey(Poll, CASCADE, "votes")

    class Meta:
        unique_together = ("poll", "voted_by")


# /        constraints = [UniqueConstraint(fields=["poll", "voted_by"], name="unique vote"), ]
