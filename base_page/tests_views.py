from django.test import TestCase, Client
from django.urls import reverse


class TestHomeView(TestCase):

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.home_url = reverse("home")

    def test_home_page_loads_successfully(self):
        """Test that the home page loads with a 200 status code."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
