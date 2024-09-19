from http.client import responses

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import reverse
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.test import APITestCase, APIClient

from account.models import Account
from poll.models import Poll, Choice


class PollTestCase(APITestCase):
    def setUp(self):
        self.db_user = Account.objects.create(username="test123")
        self.db_user.set_password("!@#$%")
        self.db_user.save()
        self.client = APIClient()

    def test_poll_non_authenticated(self):
        endpoint = "/api/v1/poll/"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_poll_list_empty(self):
        self.client.force_authenticate(self.db_user)
        endpoint = "/api/v1/poll/"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.data["previous"], None)
        self.assertEqual(response.data["next"], None)


class ChoiceTestCase(APITestCase):
    def setUp(self):
        self.db_user = Account.objects.create(username="test123")
        self.db_user.set_password("!@#$%")
        self.db_user.save()
        self.db_poll = Poll.objects.create(author=self.db_user, question="Test Poll")
        self.db_choice = Choice.objects.create(poll=self.db_poll, audio=File(open("test_files/test.mp3", 'rb')))
        self.client = APIClient()

    def test_choice_partial_update_with_valid_data(self):
        endpoint = reverse('poll:choice-detail', args=[self.db_choice.id, ])
        with open("test_files/test.mp3", "rb") as f:
            content = SimpleUploadedFile("damas.mp3", content=f.read(), content_type="audio/mp3")
        response = self.client.patch(endpoint, data={
            "audio": content
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Choice.objects.count(), 1)
        self.db_choice.refresh_from_db()
        self.assertEqual(self.db_choice.audio.path.split('/')[-1],
                         response.data["audio"].split('/')[-1])

    def test_choice_partial_update_non_valid_data(self):
        endpoint = reverse('poll:choice-detail', args=[self.db_choice.id, ])
        with open("test_files/icon.png", "rb") as f:
            content = SimpleUploadedFile("icon.png", content=f.read(), content_type="image/png")
        response = self.client.patch(endpoint, data={
            "audio": content
        })
        error = response.data["audio"][0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Choice.objects.count(), 1)
        self.db_choice.refresh_from_db()
        # self.assertEqual("invalid_extension", response.data["audio"][0][1])
        self.assertEqual("File extension “png” is not allowed. Allowed extensions are: mp3, ogg.", error)
        self.assertEqual("invalid_extension", error.code)
