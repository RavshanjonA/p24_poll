
from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from poll.models import Poll
from poll.serializers import PollSerializer, PollPatchSerializer

"""
CRUD
Create
Read
Update- >   PUT -> obyekt yaratish uchun kerak boladigan hamma fiedlar berilishi kerak.
            PATCH -> ozgartirilishi kerak bolgan fieldlar berilsa boldi.
Delete
"""


class PollsView(APIView):
    def get(self, request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PollSerializer,
        operation_description="This endpoint for creating Poll Object"
    )
    def post(self, request):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollView(APIView):
    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        serializer = PollSerializer(poll)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        serializer = PollSerializer(data=request.data, instance=poll)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "Object successfully updated"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        serializer = PollPatchSerializer(data=request.data, instance=poll)
        if serializer.is_valid():
            data = serializer.validated_data
            for key, value in data.items():
                setattr(poll, key, value)
            poll.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        poll.delete()
        return Response(data={"message": "Object successfully deleted"}, status=status.HTTP_202_ACCEPTED)
