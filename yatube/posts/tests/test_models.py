from django.test import TestCase

from ..models import Group, Post, User
from .const import (AUTHOR, GROUP_DESCRIPTION, GROUP_SLUG, GROUP_TITLE,
                    POST_TEXT)


class PostModelTest(TestCase):
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

    def test_post_model_have_correct_object_names(self):
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_group_model_have_correct_object_names(self):
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_post_verbose_name(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст публикации',
            'pub_date': 'Дата и время публикации',
            'author': 'Автор публикации',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                )

    def test_group_verbose_name(self):
        group = PostModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Префикс',
            'description': 'Краткое описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected
                )

    def test_post_help_text(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Введите текст сообщения',
            'author': 'Выберите автора публикации',
            'group': 'Выберите группу',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )

    def test_group_help_text(self):
        group = PostModelTest.group
        field_verboses = {
            'title': 'Введите название группы',
            'slug': 'Придумайте префикс для группы',
            'description': 'Введите краткое описание группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected
                )
