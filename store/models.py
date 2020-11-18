from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # products = a list of products in this category

    def __str__(self):
        return f"<Category object: {self.name} {self.id}>"


class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    desc = models.TextField()
    thumbnail = models.ImageField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Product object: {self.name} {self.id}>"

