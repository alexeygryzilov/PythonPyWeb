from django.db import models
from datetime import date, datetime, timezone
from django.core.validators import RegexValidator
from PIL import Image
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from transliterate import translit
import re

"""
Рассматриваются 4 таблицы условно обобщающие функционал блога
"""


class Blog(models.Model):
    """
    Таблица Блог, содержащая в себе
    name - название блога
    tagline - используется для хранения краткого описания или слогана блога
    """
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name="Название блога",
                            help_text="Название блога уникальное. Ограничение 100 знаков")

    slug_name = models.SlugField(unique=True,
                                 verbose_name="Slug поле названия",
                                 help_text="Название написанное транслитом, для человекочитаемости. Название уникальное.")

    headline = models.TextField(max_length=255,
                                verbose_name="Короткий слоган",
                                null=True, blank=True,
                                help_text="Ограничение 255 символов.")

    description = models.TextField(null=True, blank=True,
                                   verbose_name="Описание блога",
                                   help_text="О чем этот блог? Для кого он, в чем его ценность?")

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        unique_together = (
            'name', 'slug_name'
        )  # Условие на то, что поля 'name' и 'slug_name' должны создавать уникальную группу


class UserProfile(models.Model):
    """
    Дополнительная информация к профилю пользователя, было создано, чтобы показать, как можно
    расширить какую-то модель за счёт использования отношения
    один к одному(OneToOneField).
    user - связь с таблицей user (один к одному(у пользователя может быть только один профиль,
    соответственно профиль принадлежит определенному пользователю))
    bio - текст о себе
    avatar - картинка профиля. Стоят задачи(просто, чтобы показать как это можно решить):
        1. При сохранении необходимо переименовать картинку по шаблону user_hash
        2. Необходимо все передаваемые картинки для аватара приводить к размеру 200х200
    phone_number - номер телефона с валидацией при внесении
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    avatar = models.ImageField(upload_to='avatars/',
                               default='avatars/unnamed.png',
                               null=True,
                               blank=True)

    phone_regex = RegexValidator(
        regex=r'^\+79\d{9}$',
        message="Phone number must be entered in the format: '+79123456789'."
    )
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=12,
                                    blank=True,
                                    null=True,
                                    unique=True,
                                    help_text="Формат +79123456789",
                                    )  # максимальная длина 12 символов
    city = models.CharField(max_length=120,
                            blank=True,
                            null=True,
                            help_text="Город проживания",
                            )

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Пример переопределение метода save для изменения размера картинки
        # при сохранении в БД
        # Вызов родительского save() метода
        super().save(*args, **kwargs)

        # Открытие картинки
        image = Image.open(self.avatar.path)

        # Определение желаемого размера картинки
        desired_size = (200, 200)

        # Изменение размера
        image.thumbnail(desired_size, Image.ANTIALIAS)

        # Сохранение картинки с перезаписью
        image.save(self.avatar.path)


class AuthorProfile(models.Model):
    """
    Таблица Профиль Автора, содержащая в себе
    user - ссылка на пользователя
    bio - биография
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="author_profile")

    bio = models.TextField(blank=True,
                           null=True,
                           help_text="Короткая биография",
                           )

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль автора"
        verbose_name_plural = "Профили авторов"


def make_slug(string):
    # Удаление всех символов, не являющихся допустимыми для slug
    slug = re.sub(r'[^a-zA-Z0-9_-]', '', string)
    return slug


class Entry(models.Model):
    """
    Статья блога
    blog - связь с конкретным блогом (отношением "один ко многим" (one-to-many).
        Одна запись блога (Entry) может быть связана с одним конкретным блогом (Blog),
        но блог (Blog) может иметь множество связанных записей блога (Entry))
    headline - заголовок
    slug_headline - заголовок в транслите
    summary - краткое описание статьи
    body_text - полный текст статьи
    pub_date - дата и время публикации записи
    mod_date - дата редактирования записи
    authors - авторы написавшие данную статью (отношение "многие ко многим"
        (many-to-many). Один автор может сделать несколько записей в блог (Entry),
         и одну запись могут сделать несколько авторов (Author))
    number_of_comments - число комментариев к статье
    number_of_pingbacks -  число отзывов/комментариев на других блогах или сайтах,
        связанных с определенной записью блога (Entry)
    rating - оценка статьи
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    SCHEDULED = 'scheduled'

    STATUS_CHOICES = [
        (DRAFT, 'Черновик'),
        (PUBLISHED, 'Опубликовано'),
        (SCHEDULED, 'Отложено'),
    ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
                             related_name="entryes",
                             verbose_name="блог")  # related_name позволяет создать обратную связь
    headline = models.CharField(max_length=255,
                                verbose_name="заголовок статьи")
    slug_headline = models.SlugField(null=True,
                                     blank=True,
                                     editable=False,
                                     max_length=255,
                                     verbose_name="slug заголовок",
                                     help_text="""Если не указать, 
        то конвертирует самостоятельно, если указать, то запишет, 
        что указали (slug значение)""")  # Можно указать primary_key=True, тогда будет идентифицироваться в БД вместо id
    summary = models.TextField(verbose_name="краткое описание")
    body_text = HTMLField('текст статьи', default='', blank=True)
    image = models.ImageField(upload_to='image_entry',
                              default='image_entry/default.jpg',
                              null=True,
                              blank=True,
                              verbose_name="картинка")
    pub_date = models.DateTimeField(null=True,
                                    blank=True,
                                    verbose_name="дата публикации")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=PUBLISHED, blank=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(AuthorProfile,
                                     related_name="entrys",
                                     verbose_name="авторы",
                                     help_text="""Укажите 
                                     автора и соавторов, если они есть.
                                     Зажмите Ctrl, чтобы выделить несколько 
                                     авторов""")
    number_of_comments = models.IntegerField(default=0, blank=True)
    number_of_pingbacks = models.IntegerField(default=0, blank=True)
    rating = models.FloatField(default=0.0, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name="теги статьи")

    def save(self, *args, **kwargs):
        if self.slug_headline is None:
            # Генерация транслитерированного slug на основе headline перед сохранением
            slug_headline = "-".join(translit(self.headline, 'ru', reversed=True).lower().split())
            self.slug_headline = make_slug(slug_headline)
        if self.status in [self.SCHEDULED, self.PUBLISHED] and not self.pub_date:
            # Если запись отложена, но дата не указана, установите текущую дату
            self.pub_date = datetime.now(timezone.utc)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.headline

    class Meta:
        unique_together = ('blog', 'headline', 'slug_headline')
        ordering = ('-pub_date',)  # При выводе запроса проводить сортировку по дате
        permissions = [
            ("can_view_entry", "Может просматривать статью"),
            ("can_add_entry", "Может создать статью"),
            ("can_change_entry", "Может изменять статью"),
            ("can_delete_entry", "Может удалять статью"),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=50,
                            help_text="Ограничение на 50 символов",
                            verbose_name="Имя тега")
    slug_name = models.SlugField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='comments', null=True)
    entry = models.ForeignKey(Entry, on_delete=models.SET_NULL,
                              related_name='comments', null=True)

    text = models.TextField()

    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children',
                               verbose_name="родительский комментарий",
                               help_text="Комментарий с которого началась новая ветка",
                               )

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Дата и время создания объекта сущности в базе данных

    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата и время обновления объекта сущности в базе данных

    def __str__(self):
        return f"Пользователь: {self.user.username}; " \
               f"Статья: {self.entry.headline[:30]}; " \
               f"Текст: {self.text[:30]}"
