import re
import json
from requests import Response
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Merchant, Keyword, Transaction, EnrichedTransaction
from .serializers import CategorySerializer, MerchantSerializer, KeywordSerializer, TransactionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['get'])
    def get_transactions(self, request):
        transactions = Transaction.objects.all()
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def enrich_transactions(self, request):
        try:
            data = json.loads(request.body)
            transactions = data.get('transactions', [])

            enriched_transactions = []
            for transaction_data in transactions:
                transaction = Transaction(
                    id=transaction_data.get('id', ''),
                    description=transaction_data.get('description', ''),
                    amount=transaction_data.get('amount', 0),
                    date=transaction_data.get('date', ''),
                )

                transaction.save()
                enriched_transaction = process_enrichment(transaction_data)
                enriched_transactions.append(enriched_transaction)

            return JsonResponse({'enriched_transactions': enriched_transactions})

        except Exception as e:
            return Response(f'error: {str(e)}')

def process_enrichment(transaction_data):
    try:
        description = transaction_data.get('description', '')
        keyword_names = extract_keyword_from_description(description)
        # Buscar el comercio basado en la información de la transacción y las keywords
        merchant, keyword = find_merchant(description, keyword_names)
        # Obtener la categoría
        category = merchant.category
        # Obtener la transacción
        transaction = Transaction.objects.get(id=transaction_data['id'])

        # Crear la transacción y asignar relaciones
        enriched_transaction = EnrichedTransaction.objects.create(
            transaction=transaction,
            merchant=merchant,
            category=category,
            keyword=keyword
        )

        return {
            'id': str(enriched_transaction.id),
            'description': transaction.description,
            'amount': transaction.amount,
            'date': str(transaction.date),
            'category_name': category.name,
            'type': category.type if category else 'income' if transaction.amount > 0 else 'expense',
            'merchant_name': merchant.merchant_name if merchant else '',
            'merchant_logo': merchant.merchant_logo if merchant else '',
            'keyword': keyword.keyword if keyword else ''
        }

    except Exception as e:
        return {'error': str(e)}

def find_merchant(description, keyword_names):
    merchant = ''
    keyword = ''
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
    else:
        if not merchant and description:
            try:
                merchant = Merchant.objects.get(merchant_name__iexact=description)
                if merchant:
                    return merchant, keyword
            except Merchant.DoesNotExist:
                pass

    return merchant, keyword

def extract_keyword_from_description(description):
    words = re.findall(r'\w+', description)
    if words:
        for i in range(len(words)):
            words[i] = words[i].lower()
        return words
    return None