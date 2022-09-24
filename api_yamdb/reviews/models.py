from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_year


ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
TEN = 10

SCORES = [
    (ONE, 1),
    (TWO, 2),
    (THREE, 3),
    (FOUR, 4),
    (FIVE, 5),
    (SIX, 6),
    (SEVEN, 7),
    (EIGHT, 8),
    (NINE, 9),
    (TEN, 10),
]


class UserRole(models.Model):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    ]


class User(AbstractUser):
    username = models.TextField(
        verbose_name='Логин пользователя',
        max_length=20,
        null=True,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email пользователя',
        max_length=30,
        unique=True,
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        max_length=20,
        choices=UserRole.CHOICES,
        default=UserRole.USER,
    )

    bio = models.TextField(
        verbose_name='Информация о пользователе',
        null=True
    )
    first_name = models.TextField(
        verbose_name='Имя пользователя',
        max_length=20,
        null=True
    )
    last_name = models.TextField(
        verbose_name='Фамилия пользователя',
        max_length=20,
        null=True
    )

    class Meta:

        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название категории'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        max_length=50
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название жанра'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название произведения'
    )

    year = models.IntegerField(
        verbose_name='Год произведения',
        validators=[validate_year, ]
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        related_name='category_title',
        null=True
    )

    description = models.TextField(
        verbose_name='Описания произведения',
        blank=True,
        null=True
    )

    genres = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        related_name='reviews',
        null=True
    )
    text = models.TextField(
        'Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        related_name='reviews',
        null=True
    )
    score = models.IntegerField(
        choices=SCORES
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,)

    class Meta:

        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True
    )
    text = models.TextField(
        'Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        related_name='comments',
        null=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres_titles'
    )

    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genres_title'
    )

    class Meta:
        verbose_name = 'genre_title'
        verbose_name_plural = 'genres_titles'


class EmailAndCode(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    confirm_code = models.CharField(max_length=16)
    expire_date = models.DateTimeField(null=True)

    class Meta:
        app_label = 'api'
        verbose_name = 'email_and_code'
        verbose_name_plural = 'emails_and_codes'
