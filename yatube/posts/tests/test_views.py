import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post, User
from .const import (AUTHOR, GROUP_DESCRIPTION, GROUP_SLUG, GROUP_TITLE, IMAGE,
                    INDEX_URL, POST_TEXT, REVERSE_GROUP, REVERSE_HOME,
                    REVERSE_POST_CREATE, REVERSE_POST_DETAIL,
                    REVERSE_POST_UPDATE, REVERSE_PROFILE, TEMPLATES_PAGE_NAMES)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        title_2 = GROUP_TITLE + ' 2'
        slug_2 = GROUP_SLUG + '_2'
        description_2 = GROUP_DESCRIPTION + ' 2'
        cls.group_2 = Group.objects.create(
            title=title_2,
            slug=slug_2,
            description=description_2,
        )
        small_gif = IMAGE
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=POST_TEXT,
            group=cls.group,
            image=cls.uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        Post.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()
        cache.clear()

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_page_names = {
            'posts/index.html': REVERSE_HOME,
            'posts/group_list.html': REVERSE_GROUP,
            'posts/profile.html': REVERSE_PROFILE,
            'posts/post_detail.html': REVERSE_POST_DETAIL,
            'posts/create_post.html': REVERSE_POST_CREATE,
            'posts/update_post.html': REVERSE_POST_UPDATE,
            'core/404.html': '/unexisting_page/',
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_show_correct_context(self):
        templates_page_names = [
            REVERSE_HOME,
            REVERSE_GROUP,
            REVERSE_PROFILE,
            REVERSE_POST_DETAIL,
        ]
        for reverse_name in templates_page_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if reverse_name == REVERSE_POST_DETAIL:
                    first_object = response.context['post']
                else:
                    first_object = response.context['page_obj'][0]
                post_text = first_object.text
                post_image = first_object.image
                self.assertEqual(post_text, 'Тестовая запись')
                self.assertEqual(post_image, 'posts/small.gif')

    def test_post_image_in_db(self):
        Post.objects.create(
            author=self.user,
            text='post with image',
            group=self.group,
            image=self.uploaded,
        )
        self.assertTrue(Post.objects.filter(text='post with image').exists(),
                        'Пост с картинкой не попал в базу данных')

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(REVERSE_POST_DETAIL)
        self.assertEqual(response.context['post'].text, 'Тестовая запись')

    def test_create_or_edit_post_page_show_correct_context(self):
        templates_page_names = [
            REVERSE_POST_CREATE,
            REVERSE_POST_UPDATE,
        ]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for templat in templates_page_names:
            with self.subTest(templat=templat):
                response = self.authorized_client.get(templat)
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = (
                            response.context.get('form').fields.get(value))
                        self.assertIsInstance(form_field, expected)

    def test_post_in_incorrect_group_page(self):
        response = self.guest_client.get(reverse('posts:group_posts',
                                         kwargs={'slug': self.group_2.slug}))
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_cache_index_page(self):
        cache.clear()
        Post.objects.create(
            author=self.user,
            text='test_text_42',
            group=self.group
        )
        response = self.guest_client.get(INDEX_URL)
        self.assertIn('test_text_42', str(response.content),
                      'Пост не выводится на главную')
        response_1_authorized = self.authorized_client.get(INDEX_URL)
        response_1_guest = self.guest_client.get(INDEX_URL)
        Post.objects.filter(text='test_text_42').delete()
        self.assertFalse(Post.objects.filter(
            text='test_text_42',
        ).exists(), 'Пост не удален из базы данных')
        response_2_authorized = self.authorized_client.get(INDEX_URL)
        response_2_guest = self.guest_client.get(INDEX_URL)
        self.assertEqual(response_1_authorized.content,
                         response_2_authorized.content,
                         'Страница отдается не из кэша для '
                         'авторизованного пользователя')
        self.assertEqual(response_1_guest.content,
                         response_2_guest.content,
                         'Страница отдается не из кэша для гостя')
        cache.clear()
        response_3_authorized = self.authorized_client.get(INDEX_URL)
        response_3_guest = self.guest_client.get(INDEX_URL)
        self.assertNotEqual(response_1_authorized.content,
                            response_3_authorized.content,
                            'Удаленный пост все еще на главной '
                            'для авторизованного пользователя')
        self.assertNotEqual(response_1_guest.content,
                            response_3_guest.content,
                            'Страница отдается не из кэша для гостя')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        for i in range(13):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Тестовая запись {i}',
                group=cls.group)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Post.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()
        cache.clear()

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        for reverse_name in TEMPLATES_PAGE_NAMES:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_ten_records(self):
        for reverse_name in TEMPLATES_PAGE_NAMES:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)
