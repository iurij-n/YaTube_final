from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

User = get_user_model()


class Post(CreatedModel):

    text = models.TextField('Текст публикации',
                            help_text='Введите текст сообщения')
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Выберите автора публикации'
    )
    group = models.ForeignKey(
        'Group',
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='group_label',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        verbose_name='Картинка для поста',
        upload_to='posts/',
        blank=True,
        help_text='Картинка для поста'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.text[:15]


class Group(models.Model):

    title = models.CharField('Название группы',
                             max_length=200,
                             unique=True,
                             help_text='Введите название группы')
    slug = models.SlugField('Префикс',
                            unique=True,
                            help_text='Придумайте префикс для группы')
    description = models.TextField('Краткое описание',
                                   help_text='Введите краткое описание группы')

    def __str__(self) -> str:
        return self.title

    def get_slug(self):
        return self.slug


class Comment(CreatedModel):

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор коментария',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Выберите автора комментария'
    )
    text = models.TextField('Комментарий',
                            help_text='Введите комментарий')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text_comment[:30]


class Follow(models.Model):
    """Система подписок на отдельных авторов"""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
        help_text='Имя подписчика'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор записей',
        on_delete=models.CASCADE,
        related_name='following',
        help_text='Имя автора публикаций'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='subscribe_to_yourself'),
        ]
