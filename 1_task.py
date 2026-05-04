import pandas as pd

try:
    df = pd.read_csv('data_tallest_buildings.csv',
                     names=['name', 'height', 'year', 'floors_above', 'floors_below', 'city', 'country'],
                     encoding='utf-8')
except FileNotFoundError:
    print("Ошибка: файл data_tallest_buildings.csv не найден!")
    exit()

df['height'] = pd.to_numeric(df['height'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['floors_above'] = pd.to_numeric(df['floors_above'], errors='coerce')
df['floors_below'] = pd.to_numeric(df['floors_below'], errors='coerce')

df = df.dropna()

print("\n5 самых высоких зданий:")
highest = df.nlargest(5, 'height')
for i, row in highest.iterrows():
    print(f"  {row['name']} - {row['height']} м")

print("\n5 самых низких зданий:")
lowest = df.nsmallest(5, 'height')
for i, row in lowest.iterrows():
    print(f"  {row['name']} - {row['height']} м")

print(f"Минимальная высота: {df['height'].min()} м")
print(f"Максимальная высота: {df['height'].max()} м")
print(f"Средняя высота: {df['height'].mean()} м")
print(f"Медианная высота: {df['height'].median()} м")

country_count = df['country'].nunique()
print(f"Всего стран в файле: {country_count}")

oldest_year = df['year'].min()
oldest_buildings = df[df['year'] == oldest_year]

newest_year = df['year'].max()
newest_buildings = df[df['year'] == newest_year]

print(f"Самые старые здания ({oldest_year} год):")
for i, row in oldest_buildings.iterrows():
    print(f"  {row['name']} - {row['city']}, {row['country']}")

print(f"\nСамые новые здания ({newest_year} год):")
for i, row in newest_buildings.iterrows():
    print(f"  {row['name']} - {row['city']}, {row['country']}")


try:
    threshold = int(input("Введите количество этажей (сумма надземных и подземных): "))
except ValueError:
    print("Ошибка! Введите целое число.")
    exit()

df['total_floors'] = df['floors_above'] + df['floors_below']
buildings_with_more_floors = df[df['total_floors'] > threshold]

if len(buildings_with_more_floors) > 0:
    print(f"\nЗданий с суммой этажей > {threshold}: {len(buildings_with_more_floors)}")
    result = buildings_with_more_floors[['name', 'total_floors', 'city', 'country']]
    print(result.to_string(index=False))
else:
    print(f"\nНет зданий с суммой этажей больше {threshold}")


try:
    target_year = int(input("Введите год постройки: "))
except ValueError:
    print("Ошибка! Введите целое число.")
    exit()

buildings_in_target_year = df[df['year'] == target_year]

if len(buildings_in_target_year) > 0:
    print(f"\nЗдания, построенные в {target_year} году:")
    for i, row in buildings_in_target_year.iterrows():
        print(f"  {row['name']} - {row['city']}, {row['country']} (высота: {row['height']} м)")
else:
    print(f"\nНет зданий, построенных в {target_year} году")


target_country = input("Введите название страны: ")
buildings_in_country = df[df['country'].str.lower() == target_country.lower()]
count = len(buildings_in_country)

if count > 0:
    print(f"\nВ стране '{target_country}' находится {count} зданий:")
    for i, row in buildings_in_country.iterrows():
        print(f"  {row['name']} - {row['city']} ({row['height']} м, {row['year']} год)")
else:
    print(f"\nВ стране '{target_country}' нет зданий в списке или страна не найдена")