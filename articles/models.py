from django.db import models
from django.conf import settings

class Article(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'

    VISIBILITY_CHOICES = [
        (PUBLIC, 'Публичная'),
        (PRIVATE, 'Закрытая'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default=PUBLIC,
    )

    def __str__(self):
        return self.title
