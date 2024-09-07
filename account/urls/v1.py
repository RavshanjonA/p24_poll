from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views import AccountView, InterestView

router = DefaultRouter()
router.register('interest', InterestView, basename='interest')
router.register('', AccountView, basename="account")

urlpatterns = [
    path('', include(router.urls)),
    # path('interest/', InterestView.as_view({"get":'list'})),
]
