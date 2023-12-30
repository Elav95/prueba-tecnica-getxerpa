import pandas as pd
from enrichment.models import Transaction, Category, Merchant, Keyword

def run():
    excel_file_path = 'data/data.xlsx'

    try:
        # Categories
        df_categories = pd.read_excel(excel_file_path, sheet_name='Categorías')
        for _, row in df_categories.iterrows():
            Category.objects.create(
                id=row['id'],
                name=row['name'],
                type=row['type'],
            )

        # Merchant
        df_merchants = pd.read_excel(excel_file_path, sheet_name='Comercios')
        for _, row in df_merchants.iterrows():
            Merchant.objects.create(
                id=row['id'],
                merchant_name=row['merchant_name'],
                merchant_logo=row['merchant_logo'],
                category_id=row['category_id'] if row['category_id'] else None,
            )

        # Keywords
        df_keywords = pd.read_excel(excel_file_path, sheet_name='Keywords')
        for _, row in df_keywords.iterrows():
            Keyword.objects.create(
                id=row['id'],
                keyword=row['keyword'],
                merchant_id=row['merchant_id'] if row['merchant_id'] else None,
            )

        print('Data imported successfully!')

    except Exception as e:
        print(f'Error: {e}')
