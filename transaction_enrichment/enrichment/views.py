import re
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Merchant, Keyword, Transaction, EnrichedTransaction
from .serializers import CategorySerializer, MerchantSerializer, KeywordSerializer, TransactionSerializer, EnrichedTransactionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    # CRUD operations for Category model
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MerchantViewSet(viewsets.ModelViewSet):
    # CRUD operations for Merchant model
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    # CRUD operations for Keyword model
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    # CRUD operations for Transaction model
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def enrich_transactions(self, request):
        # Custom action to enrich transactions with additional information
        try:
            status_code = 200
            data = json.loads(request.body)
            transactions = data.get('transactions', [])
            enriched_transactions = []

            for transaction_data in transactions:
                transaction_id = transaction_data.get('id', None)
                try:
                    # Check if the provided ID is already in use
                    transaction = Transaction.objects.get(id=transaction_id)
                    if (
                        transaction.description != transaction_data.get('description') or
                        transaction.amount != transaction_data.get('amount') or
                        str(transaction.date) != transaction_data.get('date')
                    ):
                        enriched_transactions.append({'Error': f'Transaction with ID {transaction_id} already exists with different values.'})
                        status = 207
                        continue
                except ObjectDoesNotExist:
                    serializer = TransactionSerializer(data=transaction_data)
                    if serializer.is_valid():
                        # If the ID is provided and not in use, use it; otherwise, let Django generate a new one
                        transaction = serializer.save() if not transaction_id else serializer.save(id=transaction_id)
                    else:
                        enriched_transactions.append({'Error': 'Invalid data'})
                        status = 207
                        continue

                enriched_transaction_data = process_enrichment(transaction)
                enriched_transactions.append(enriched_transaction_data)

            return JsonResponse({'enriched_transactions': enriched_transactions}, status=status_code)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def process_enrichment(transaction):
    # Process and enrich a transaction with additional information
    try:
        description = transaction.description
        keyword_names = extract_keyword_from_description(description)
        merchant, keyword = find_merchant(description, keyword_names)
        category = merchant.category if merchant and merchant.category else None

        EnrichedTransaction.objects.update_or_create(transaction=transaction,
            defaults={
                'merchant': merchant,
                'category': category,
                'keyword': keyword
            }
        )

        return {
            'transaction_id': transaction.id,
            'description': transaction.description,
            'amount': transaction.amount,
            'date': transaction.date,
            'category_name': category.name if category else None,
            'type': category.type if category else 'income' if transaction.amount > 0 else 'expense',
            'merchant_name': merchant.merchant_name if merchant else None,
            'merchant_logo': merchant.merchant_logo if merchant else None,
            'keyword': keyword.keyword if keyword else None
        }

    except Exception as e:
        return {'error': str(e)}

def find_merchant(description, keyword_names):
    # Find a merchant based on the information from the transaction and keywords
    merchant = None
    keyword = None
    if keyword_names:
        for word in keyword_names:
            try:
                keyword = Keyword.objects.get(keyword=word)
                if keyword and keyword.merchant_id:
                    merchant_id = keyword.merchant_id
                    merchant = Merchant.objects.get(id=merchant_id)
                    return merchant, keyword
            except Keyword.DoesNotExist:
                pass
            except Merchant.DoesNotExist:
                pass

    if not merchant and description:
        try:
            merchant = Merchant.objects.get(merchant_name__iexact=description)
            if merchant:
                return merchant, keyword
        except Merchant.DoesNotExist:
            pass

    return merchant, keyword

def extract_keyword_from_description(description):
    # Extract keywords from the transaction description
    words = re.findall(r'\w+', description)
    if words:
        return [word.lower() for word in words]
    return None