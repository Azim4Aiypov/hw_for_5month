from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(default=1)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Review {self.id} for {self.product.title}'
