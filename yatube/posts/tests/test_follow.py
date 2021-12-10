from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Group, Post, User
from .const import GROUP_DESCRIPTION, GROUP_SLUG, GROUP_TITLE, POST_TEXT


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create(username='John')
        cls.user2 = User.objects.create(username='Bob')
        cls.user3 = User.objects.create(username='Tim')
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user2,
            text=POST_TEXT,
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Post.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()
        Follow.objects.all().delete()
        cache.clear()

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)
        self.authorized_client_1 = Client()
        self.authorized_client_1.force_login(self.user3)

    def test_create_and_delete_follow(self):
        foll_count_1 = Follow.objects.all().count()
        self.authorized_client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': self.user2.username, }))
        foll_count_2 = Follow.objects.all().count()
        self.assertEqual(foll_count_2,
                         foll_count_1 + 1, 'Запись в таблице '
                                           'подписок не создана')
        self.authorized_client.get(
            reverse('posts:profile_unfollow',
                    kwargs={'username': self.user2.username, }))
        foll_count_2 = Follow.objects.all().count()
        self.assertEqual(foll_count_2, foll_count_1, 'Запись в таблице '
                                                     'подписок не удалена')

    def test_post_in_feed(self):
        Follow.objects.create(
            user=self.user1,
            author=self.user2
        )
        Post.objects.create(
            author=self.user2,
            text='test_text_42',
            group=self.group
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertIn('test_text_42', str(response.content),
                      'Пост не выводится в ленту подписчика')
        response = self.authorized_client_1.get(reverse('posts:follow_index'))
        self.assertNotIn('test_text_42', str(response.content),
                         'Пост выводится в ленту неподписчика')
