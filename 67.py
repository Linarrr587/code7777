import json
from datetime import datetime, timedelta
import os
FILE_NAME = "purchases.json"
purchases = []

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
def print_table(data):
    if not data:
        print("Список пуст")
        return
    print("\n{:<5} {:<20} {:<10} {:<15} {:<12}".format(
        "№", "Название", "Цена", "Категория", "Дата"
    ))
    print("-" * 65)
    for i, p in enumerate(data, 1):
        print("{:<5} {:<20} {:<10.2f} {:<15} {:<12}".format(
            i, p["name"], p["price"], p["category"], p["date"]
        ))

# ===== УПРАВЛЕНИЕ ПОКУПКАМИ =====
def add_purchase():
    name = input("Название товара: ")
    try:
        price = float(input("Цена: "))
    except ValueError:
        print("Ошибка: цена должна быть числом")
        return
    category = input("Категория: ")
    date_input = input("Дата (ГГГГ-ММ-ДД, Enter = сегодня): ")

    if date_input == "":
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
        except ValueError:
            print("Неверный формат даты")
            return
    purchases.append({
        "name": name,
        "price": price,
        "category": category,
        "date": date
    })
    print("Покупка добавлена")
def view_purchases():
    print_table(purchases)
def delete_purchase():
    view_purchases()
    if not purchases:
        return
    try:
        index = int(input("Введите номер покупки для удаления: "))
        if 1 <= index <= len(purchases):
            removed = purchases.pop(index - 1)
            print(f"Удалено: {removed['name']}")
        else:
            print("Неверный номер")
    except ValueError:
        print("Введите число")
def search_purchase():
    keyword = input("Введите название для поиска: ").lower()
    results = [p for p in purchases if keyword in p["name"].lower()]
    print_table(results)
def sort_purchases():
    print("Сортировка:")
    print("1. По цене")
    print("2. По дате")
    choice = input("Выберите вариант: ")
    if choice == "1":
        purchases.sort(key=lambda x: x["price"])
    elif choice == "2":
        purchases.sort(key=lambda x: x["date"])
    else:
        print("Неверный выбор")
        return
    print("Список отсортирован")

# ===== АНАЛИЗ =====
def total_spent():
    total = sum(p["price"] for p in purchases)
    print(f"Общие расходы: {total:.2f}")
def spent_by_category():
    result = {}
    for p in purchases:
        result[p["category"]] = result.get(p["category"], 0) + p["price"]
    print("\nРасходы по категориям:")
    for cat, amount in result.items():
        print(f"{cat}: {amount:.2f}")
def spent_by_period():
    print("Период:")
    print("1. День")
    print("2. Неделя")
    print("3. Месяц")
    choice = input("Выберите период: ")
    now = datetime.now()
    if choice == "1":
        start_date = now - timedelta(days=1)
    elif choice == "2":
        start_date = now - timedelta(days=7)
    elif choice == "3":
        start_date = now - timedelta(days=30)
    else:
        print("Неверный выбор")
        return
    filtered = []
    total = 0
    for p in purchases:
        p_date = datetime.strptime(p["date"], "%Y-%m-%d")
        if p_date >= start_date:
            filtered.append(p)
            total += p["price"]
    print_table(filtered)
    print(f"Сумма за период: {total:.2f}")
    
# ===== ФАЙЛЫ =====
def save_data():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(purchases, f, ensure_ascii=False, indent=4)
        print("Данные сохранены")
    except Exception as e:
        print("Ошибка сохранения:", e)
def load_data():
    global purchases
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                purchases = json.load(f)
            print("Данные загружены")
        except Exception:
            print("Ошибка загрузки, создаётся новый список")
            purchases = []
    else:
        purchases = []

# ===== МЕНЮ =====
def main():
    load_data()
    while True:
        print("\n=== МЕНЮ ===")
        print("1. Добавить покупку")
        print("2. Показать покупки")
        print("3. Общие расходы")
        print("4. По категориям")
        print("5. За период")
        print("6. Поиск")
        print("7. Удалить")
        print("8. Сортировать")
        print("9. Сохранить")
        print("0. Выход")
        choice = input("Выберите пункт: ")
        if choice == "1":
            add_purchase()
        elif choice == "2":
            view_purchases()
        elif choice == "3":
            total_spent()
        elif choice == "4":
            spent_by_category()
        elif choice == "5":
            spent_by_period()
        elif choice == "6":
            search_purchase()
        elif choice == "7":
            delete_purchase()
        elif choice == "8":
            sort_purchases()
        elif choice == "9":
            save_data()
        elif choice == "0":
            save_data()
            print("Выход из программы")
            break
        else:
            print("Неверный ввод")
if __name__ == "__main__":
    main()
