from django.urls import path

from poll.views import PollsView, PollView

urlpatterns = [
    path("", PollsView.as_view(), name="poll-list"),
    path("<int:pk>/", PollView.as_view(), name="poll-detail"),
]
