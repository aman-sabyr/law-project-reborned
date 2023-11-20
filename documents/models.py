from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string


User = get_user_model()


class DocumentManager(models.Manager):

    def _create(self, **extra_fields):
        extra_fields.update({'slug': get_random_string(7)})
        document = self.model(extra_fields)
        document.save()
        return document

    def create_document(self, **extra_fields):
        return self._create(**extra_fields)


class Document(models.Model):
    slug = models.SlugField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=1024, verbose_name='documents name')
    link = models.TextField(verbose_name='link on cloud to this document')
    created_at = models.DateTimeField(auto_now=True, verbose_name='was created')
    modified_at = models.DateTimeField(verbose_name='last time it was modified')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='was created by')

    def __str__(self):
        return f'{self.slug}'


class ChangeManager(models.Manager):
    def _create(self):
        pass

    def create_change(self, ):
        pass


class Change(models.Model):
    slug = models.SlugField(max_length=5, unique=True, primary_key=True, verbose_name='change\'s slug')
    parent_change = models.CharField(max_length=5, verbose_name='slug of the parent\'s change')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='documents slug')
    selected_text = models.TextField(verbose_name='text that should be changed')
    modified_text = models.TextField(verbose_name='text that should be inserted')
    created_at = models.DateTimeField(auto_now=True, verbose_name='was created')
    modified_at = models.DateTimeField(verbose_name='last time it was modified')
    user = models.ForeignKey(User, verbose_name='was created by')

    def __str__(self):
        return f'{self.slug}'



