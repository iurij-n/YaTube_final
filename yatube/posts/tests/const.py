from django.urls import reverse

AUTHOR = 'auth'
GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test_slug'
GROUP_DESCRIPTION = 'Тестовое описание'
POST_TEXT = 'Тестовая запись'

INDEX_URL = '/'
ABOUT_AUTHOR_URL = '/about/author/'
ABOUT_TECH_URL = '/about/tech/'
GROUP_URL = '/group/' + GROUP_SLUG + '/'
PROFILE_URL = '/profile/' + AUTHOR + '/'
CREATE_URL = '/create/'
POST_URL = '/posts/'
EDIT_URL = '/edit/'

REVERSE_HOME = reverse('posts:home')
REVERSE_GROUP = reverse('posts:group_posts', kwargs={'slug': GROUP_SLUG})
REVERSE_PROFILE = reverse('posts:profile', kwargs={'username': AUTHOR})
REVERSE_POST_DETAIL = reverse('posts:post_detail', kwargs={'post_id': '1'})
REVERSE_POST_CREATE = reverse('posts:post_create')
REVERSE_POST_UPDATE = reverse('posts:post_edit', kwargs={'post_id': '1'})
TEMPLATES_PAGE_NAMES = [
    REVERSE_HOME,
    REVERSE_GROUP,
    REVERSE_PROFILE,
]
IMAGE = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
         b'\x01\x00\x80\x00\x00\x00\x00\x00'
         b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
         b'\x00\x00\x00\x2C\x00\x00\x00\x00'
         b'\x02\x00\x01\x00\x00\x02\x02\x0C'
         b'\x0A\x00\x3B'
         )
