from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from account.models import Account, Interest
from account.serializers import AccountSerializer, InterestSerializer, AccountDetialSeriaizer


class AccountView(ModelViewSet):
    # serializer_class = AccountSerializer
    queryset = Account.objects.all()
    serializer_class2 = AccountDetialSeriaizer

    # create list -> AccountSerializer
    # detail, put, patch, delete -> AccountDetailSerializer
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
        serializer = self.serializer_class2(data=request.data, instance=account, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class InterestView(ViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

    def list(self, request):
        serializer = InterestSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        interest = get_object_or_404(Interest, pk=pk)
        serializer = self.serializer_class(instance=interest, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
