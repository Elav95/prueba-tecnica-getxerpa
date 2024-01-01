import json
from django.test import TestCase
from rest_framework import status
from .models import Category, Merchant, Keyword, Transaction

class YourAppTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.base_dir = 'http://127.0.0.1:8000/api'
        self.category = Category.objects.create(name='Test Category', type='expense')
        self.merchant = Merchant.objects.create(merchant_name='Test Merchant', category=self.category)
        self.keyword = Keyword.objects.create(keyword='test', merchant=self.merchant)
        self.transaction = Transaction.objects.create(
            description='Test Transaction',
            amount=-100.0,
            date='2024-01-01'
        )
    def test_keyword_crud_operations(self):
        # Test Keyword CRUD operations
        keyword_url = self.base_dir + '/keywords/'
        data = {'keyword': 'NewKeyword'}

        # Create Keyword
        response = self.client.post(keyword_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve Keywords
        response = self.client.get(keyword_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_merchant_crud_operations(self):
        # Test Merchant CRUD operations
        merchant_url = self.base_dir + '/merchants/'
        data = {'merchant_name': 'New Merchant', 'merchant_logo': ''}

        # Create Merchant
        response = self.client.post(merchant_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve Merchants
        response = self.client.get(merchant_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_crud_operations(self):
        category_url = self.base_dir + '/categories/'
        # Test Category CRUD operations
        data = {'name': 'New Category', 'type': 'expense'}
        
        # Create Category
        response = self.client.post(category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve Category
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transaction_crud_operations(self):
        # Test Transaction CRUD operations
        transaction_url = self.base_dir + '/transactions/'
        data = {'description' : 'Another Transaction', 'amount' : -140.0,'date': '2024-01-01'}

        # Create Transaction
        response = self.client.post(transaction_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve Transactions
        response = self.client.get(transaction_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transaction_enrichment(self):
        # Test enrich_transactions custom action
        url = self.base_dir + '/transactions/enrich_transactions/'
        data = {'transactions': [{'id': 1, 'description': 'Another Test Transaction', 'amount': -50.0, 'date': '2024-01-01'}]}
        
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIsNotNone(response['enriched_transactions'][0]["category_name"])
        self.assertIsNotNone(response['enriched_transactions'][0]["type"])
        self.assertIsNotNone(response['enriched_transactions'][0]["merchant_name"])
        self.assertIsNotNone(response['enriched_transactions'][0]["keyword"])
