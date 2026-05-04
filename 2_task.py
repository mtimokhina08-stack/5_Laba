import pandas as pd

try:
    products = pd.read_csv('products.csv', encoding='utf-8')
except FileNotFoundError:
    print("Ошибка: файл products.csv не найден!")
    exit()

try:
    sales = pd.read_csv('sales.csv', encoding='utf-8')
except FileNotFoundError:
    print("Ошибка: файл sales.csv не найден!")
    exit()

sales['price'] = pd.to_numeric(sales['price'], errors='coerce')
sales['quantity'] = pd.to_numeric(sales['quantity'], errors='coerce')
sales['product_id'] = pd.to_numeric(sales['product_id'], errors='coerce')
products['product_id'] = pd.to_numeric(products['product_id'], errors='coerce')

data = pd.merge(sales, products, on='product_id', how='inner')

data['revenue'] = data['price'] * data['quantity']

revenue_by_category = data.groupby('category')['revenue'].sum()

# Превращаем результат в DataFrame для удобного сохранения
result_table = revenue_by_category.reset_index()
result_table.columns = ['category', 'revenue']

try:
    result_table.to_csv('result.csv', index=False, encoding='utf-8')
    print("Результат сохранён в файл result.csv")
except Exception as e:
    print(f"\nОшибка при сохранении файла: {e}")