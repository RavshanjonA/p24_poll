
from rest_framework import serializers

from account.models import Account
from poll.models import Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("id", "question", "author", "published")


class PollPatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(required=False)
    author = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)


