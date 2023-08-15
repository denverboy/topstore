from django.db import models


def category_img_directory_path(instance, filename):
    return f'categories/category-{instance.title}/{filename}'


class Category(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=category_img_directory_path
    )
    subcategories = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
