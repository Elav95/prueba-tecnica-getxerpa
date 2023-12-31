from rest_framework import serializers
from .models import Category, Merchant, Keyword, Transaction, EnrichedTransaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class EnrichedTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrichedTransaction
        fields = '__all__'