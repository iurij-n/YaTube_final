from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Group, Post, User
from .const import (ABOUT_TECH_URL, AUTHOR, CREATE_URL, EDIT_URL,
                    GROUP_DESCRIPTION, GROUP_SLUG, GROUP_TITLE, GROUP_URL,
                    INDEX_URL, POST_TEXT, POST_URL, PROFILE_URL)


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=POST_TEXT,
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_page_exist_at_desired_location(self):
        post = PostURLTest.post
        page_url = (INDEX_URL,
                    ABOUT_TECH_URL,
                    GROUP_URL,
                    PROFILE_URL,
                    POST_URL + str(post.pk) + '/',
                    '/unexisting_page/'
                    )
        for url in page_url[-2::-1]:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get(page_url[-1])
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_page_exist_at_desired_location_for_autorized_user(self):
        response = self.authorized_client.get(CREATE_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_exist_at_desired_location_for_autor(self):
        post = PostURLTest.post
        response = self.authorized_client.get(
            POST_URL + str(post.pk) + EDIT_URL
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_exist_uses_correct_template(self):
        post = PostURLTest.post
        page_template = {
            INDEX_URL: 'posts/index.html',
            GROUP_URL: 'posts/group_list.html',
            PROFILE_URL: 'posts/profile.html',
            POST_URL + str(post.pk) + '/': 'posts/post_detail.html',
            POST_URL + str(post.pk) + EDIT_URL: 'posts/update_post.html',
            CREATE_URL: 'posts/create_post.html',
        }
        for url, template in page_template.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
