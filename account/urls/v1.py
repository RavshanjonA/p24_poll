from django.urls import include, path
from rest_framework.routers import DefaultRouter

from account.views import AccountView, InterestView, PermissionViewSet, GroupViewSet

router = DefaultRouter()
router.register("interest", InterestView, basename="interest")
router.register("group", GroupViewSet, basename="group")
router.register("permission", PermissionViewSet, basename="permission")
router.register("", AccountView, basename="account")
app_name = "account"
urlpatterns = [
    path("", include(router.urls)),
    # path('interest/', InterestView.as_view({"get":'list'})),
]
