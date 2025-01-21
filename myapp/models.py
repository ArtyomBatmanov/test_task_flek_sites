from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from PIL import Image
import os
import uuid
from django.utils.text import slugify
from django.core.files.storage import default_storage
import io
from django.core.files.base import ContentFile





def avatar_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.first_name)}_{uuid.uuid4().hex}.{ext}"
    return os.path.join('avatars/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    organizations = models.ManyToManyField('Organization', related_name='members')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


    def save(self, *args, **kwargs):
        if self.avatar and not self.avatar.name.startswith('avatars/'):
            old_avatar = self.avatar.name  # Сохраняем старое имя для удаления
            self.avatar.name = avatar_upload_to(self, self.avatar.name)

            # Удаляем старый файл, если он существует
            if old_avatar and default_storage.exists(old_avatar):
                default_storage.delete(old_avatar)

            # Открываем изображение и изменяем размер
            img = Image.open(self.avatar)
            img.thumbnail((200, 200))  # Изменение размера до 200x200

            # Сохраняем измененное изображение в памяти
            output = io.BytesIO()
            img_format = 'JPEG' if img.format == 'JPEG' else 'PNG'
            img.save(output, format=img_format)
            output.seek(0)

            # Заменяем оригинальный файл новым уменьшенным
            self.avatar = ContentFile(output.read(), name=self.avatar.name)

        super().save(*args, **kwargs)


class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
