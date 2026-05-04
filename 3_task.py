import pandas as pd

try:
    df = pd.read_csv('stores.csv', encoding='utf-8')
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    print("Ошибка: файл stores.csv не найден!")
    exit()

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
df = df.dropna()

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month


monthly_sales = df.groupby(['store', 'year', 'month'])['sales'].sum()
dynamics = monthly_sales.reset_index()
dynamics['year_month'] = dynamics['year'].astype(str) + '-' + dynamics['month'].astype(str)
pivot_dynamics = dynamics.pivot_table(index='store', columns='year_month', values='sales')


best_months_list = []
for store in df['store'].unique():
    store_monthly = monthly_sales[store]

    max_sales = store_monthly.max()

    best_months = store_monthly[store_monthly == max_sales]

    for (year, month), sales in best_months.items():
        best_months_list.append({
            'store': store,
            'year': year,
            'month': month,
            'month_name': f"{month}-й месяц",
            'sales': sales
        })

best_months_df = pd.DataFrame(best_months_list)


try:
    selected_year = int(input("Введите год для рейтинга: "))
except ValueError:
    print("Ошибка! Введите целое число")

yearly_sales = dynamics[dynamics['year'] == selected_year].groupby('store')['sales'].sum()

if len(yearly_sales) > 0:
    rating = yearly_sales.sort_values(ascending=False)
    rating_df = rating.reset_index()
    rating_df.columns = ['store', 'total_sales']
else:
    rating_df = pd.DataFrame(columns=['store', 'total_sales'])

try:
    with pd.ExcelWriter('stores_report.xlsx', engine='openpyxl') as writer:
        pivot_dynamics.to_excel(writer, sheet_name='Динамика_по_месяцам')

        best_months_df[['store', 'year', 'month_name', 'sales']].to_excel(
            writer, sheet_name='Лучший_месяц', index=False)

        rating_df.to_excel(writer, sheet_name='Рейтинг_за_год', index=False)

    print("Результат сохранён в файл stores_report.xlsx")

except Exception as e:
    print(f"Ошибка при сохранении: {e}")