from django.db import models

class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('expense', 'Expense'), ('income', 'Income')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    merchant_name = models.CharField(max_length=255)
    merchant_logo = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Keyword(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    keyword = models.CharField(max_length=255)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)