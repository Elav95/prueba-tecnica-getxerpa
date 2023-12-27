from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20)

class Merchant(models.Model):
    merchant_name = models.CharField(max_length=255)
    merchant_logo = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Keyword(models.Model):
    keyword = models.CharField(max_length=255)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)

class Transaction(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()