from django.urls import path

from poll.views import PollsView, PollView, RegisterView

urlpatterns = [
    path("", PollsView.as_view(), name="poll-list"),
    path("<int:pk>/", PollView.as_view(), name="poll-detail"),
    path("register/", RegisterView.as_view(), name="user-register")
]
