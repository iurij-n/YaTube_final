from http import HTTPStatus

from django.test import Client, TestCase

from .const import ABOUT_AUTHOR_URL, ABOUT_TECH_URL


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_page_exist_at_desired_location(self):
        page_url = (ABOUT_AUTHOR_URL,
                    ABOUT_TECH_URL)
        for url in page_url:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
