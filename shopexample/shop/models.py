import random
from string import ascii_letters, digits

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug() -> str:
    """
    Generate a random slug consisting of 3 alphanumeric characters.
    """
    return "".join([random.choice(ascii_letters + digits) for _ in range(3)])


class Category(models.Model):
    """
    Represents a category for organizing products.
    """
    name = models.CharField(max_length=124, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    slug = models.SlugField(max_length=140, unique=True, null=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_list', args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Save the category instance to the database.
        """
        if not self.slug:
            self.slug = slugify(rand_slug() + self.name)
        super().save(*args, **kwargs)


class ProductManage(models.Manager):
    """
    Custom manager for the Product model to filter available products.
    """
    def get_queryset(self):
        """
        Return a queryset of available products.
        """
        return super().get_queryset().filter(available=True)


class Product(models.Model):
    """
    Represents a product in the catalog.
    """
    title = models.CharField(max_length=248, db_index=True)
    slug = models.SlugField(max_length=264, unique=True)
    brand = models.CharField(max_length=248)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField(upload_to='products/products/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    availability = ProductManage()
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def __str__(self):
        return self.title
