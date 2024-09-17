from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from account.models import Account


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
