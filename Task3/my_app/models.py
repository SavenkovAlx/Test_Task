from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема поста')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to=user_directory_path, verbose_name='Фото')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    description = models.TextField(verbose_name='Текст комментария')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
