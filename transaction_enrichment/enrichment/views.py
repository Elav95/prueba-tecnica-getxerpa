import json
from uuid import uuid4
from requests import Response
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Merchant, Keyword, Transaction, extract_keyword_from_description
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
                    description=transaction_data.get('description', ''),
                    amount=transaction_data.get('amount', 0),
                    date=transaction_data.get('date', ''),
                )

                transaction.save()
                enriched_transaction = process_enrichment(transaction_data)
                enriched_transactions.append(enriched_transaction)

            return JsonResponse({'enriched_transactions': enriched_transactions})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def process_enrichment(transaction_data):
    try:
        description = transaction_data.get('description', '')
        keyword_name = extract_keyword_from_description(description)

        # Buscar el comercio basado en la información de la transacción y las keywords
        merchant = find_merchant(description, keyword_name)

        # Obtener o crear la categoría
        category_name = transaction_data.get('category_name', '')
        category_type = 'expense' if transaction_data.get('amount', 0) < 0 else 'income'
        category, category_created = Category.objects.get_or_create(
            name=category_name,
            defaults={'type': category_type}
        )

        # Crear la transacción y asignar relaciones
        transaction = Transaction.objects.create(
            description=description,
            amount=transaction_data.get('amount', 0),
            date=transaction_data.get('date'),
            merchant=merchant,
            category=category,
            keyword=Keyword.objects.get_or_create(name=keyword_name)[0]
        )

        return {
            'id': str(transaction.id),
            'description': transaction.description,
            'amount': transaction.amount,
            'date': str(transaction.date),
            'category_name': category.name,
            'type': category.type,
            'merchant_name': merchant.name if merchant else None,
            'merchant_logo': merchant.logo if merchant else None,
            'keyword': keyword_name,
            'merchant_id': str(merchant.id) if merchant else None
        }

    except Exception as e:
        return {'error': str(e)}

def find_merchant(description, keyword_name):
    merchant = None
    if keyword_name:
        for word in keyword_name:
            keyword = Keyword.objects.get(keyword=word)
            if keyword:
                try:
                    id = keyword.merchant
                    merchant = Merchant.objects.get(id=id)
                except Merchant.DoesNotExist:
                    pass
    else:
        if not merchant and description:
            try:
                merchant = Merchant.objects.get(name__iexact=description)
            except Merchant.DoesNotExist:
                pass

    return merchant