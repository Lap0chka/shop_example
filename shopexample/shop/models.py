import random

from django.db import models
from django.utils.text import slugify
from string import ascii_letters, digits


def rand_slug():
    return "".join([random.choice(ascii_letters+digits) for _ in range(3)])


class Categories(models.Model):
    name = models.CharField(max_length=124, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True
    )
    slug = models.SlugField(max_length=140, unique=True, null=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + self.name)
        super().save()
