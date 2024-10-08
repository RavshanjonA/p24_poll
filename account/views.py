from re import search
from trace import Trace

from django.contrib.auth.models import Group, Permission
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from yaml import serialize

from account.models import Account, Interest
from account.search import CustomSearchFilter
from account.serializers import (AccountDetailSerializer, AccountSerializer,
                                 InterestSerializer, GroupSerializer, PermissionSerializer, UserPermissionSerializer)


class AccountView(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all().order_by("id")
    serializer_class2 = AccountDetailSerializer
    my_tags = ("account",)
    filter_backends = (CustomSearchFilter,)
    # filter_backends = (SearchFilter,)
    search_fields = ("username", "email", "phone")
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("phone", None)
        if search:
            queryset = queryset.filter(phone__contains=search)
        return queryset

    @action(methods=["get"], detail=True)
    def interests(self, *args, **kwargs):
        account = self.get_object()
        serializer = InterestSerializer(account.profile.interests.all(), many=True)
        return Response(data=serializer.data)

        # api/v1/account/top-contacts/

    @action(methods=["POST"], detail=False, url_path="top-accounts")
    def top_accounts(self, *args, **kwargs):
        queryset = self.get_queryset()
        # queryset = queryset.filter(profile__interests__isnull=False).distinct()
        queryset = (
            queryset.annotate(interest_count=Count("profile__interests"))
            .filter(interest_count__gt=0)
            .order_by("-interest_count")
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"], detail=True, url_path="permissions")
    def permissions(self, *args, **kwargs):
        user = self.get_object()
        serializer = UserPermissionSerializer(user.user_permissions.all(), many=True)
        return Response(data=serializer.data)

    def retrieve(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class2(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class2(data=request.data, instance=account)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, pk=None):
        account = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class2(
            data=request.data, instance=account, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class InterestView(ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    my_tags = ("interest",)

    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)

    def get_queryset(self):
        queryset = Interest.objects.all()
        search = self.request.query_params.get("search")
        if search:
            queryset = Interest.objects.annotate(similarity=TrigramSimilarity('name', search)).filter(
                similarity__gte=0.1).order_by('-similarity')
        return queryset

    def list(self, request):
        serializer = InterestSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        interest = get_object_or_404(Interest, pk=pk)
        serializer = self.serializer_class(
            instance=interest, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    my_tags = ("group",)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by("id")
    serializer_class = PermissionSerializer
    my_tags = ("permission",)

    APP_LABELS = {"account", "poll"}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(content_type__app_label__in=self.APP_LABELS)
        return queryset
