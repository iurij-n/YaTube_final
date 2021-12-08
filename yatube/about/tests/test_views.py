from django.test import Client, TestCase

from .const import ABOUT_AUTHOR_URL, ABOUT_TECH_URL


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_page_exist_uses_correct_template(self):
        page_template = {
            'about/author.html': ABOUT_AUTHOR_URL,
            'about/tech.html': ABOUT_TECH_URL,
        }
        for template, url in page_template.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
