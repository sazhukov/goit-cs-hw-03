from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from bson import ObjectId

# Підключення до MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/") # MongoDB URI
    # client = MongoClient("mongodb+srv://sazhukov:<mecoft06>@cluster0.gomeg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") # MongoDB URI
    db = client["cat_database"]  # Вкажіть свою базу даних
    collection = db["cats"]  # Вкажіть свою колекцію
    # Перевірка з'єднання
    client.admin.command('ismaster')
    print("MongoDB підключено успішно")
except ConnectionFailure:
    print("Не вдалося підключитися до MongoDB, перевірте з'єднання")


def create_document():
    try:
        name = input("Введіть ім'я тварини: ")
        age = int(input("Введіть вік тварини: "))
        features = input("Введіть характеристики тварини (через кому): ").split(",")
        cat = {"name": name, "age": age, "features": [feature.strip() for feature in features]}
        collection.insert_one(cat)
        print(f"Документ створено для тварини {name}.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")
    except ValueError as e:
        print(f"Помилка введення: {e}")


def read_all_documents():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def read_document_by_name():
    try:
        name = input("Введіть ім'я тварини для пошуку: ")
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Тварину з ім'ям {name} не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def update_document_age():
    try:
        name = input("Введіть ім'я тварини, щоб оновити її вік: ")
        new_age = int(input("Введіть новий вік тварини: "))
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Вік тварини {name} оновлено.")
        else:
            print(f"Тварину з ім'ям {name} не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")
    except ValueError as e:
        print(f"Помилка введення: {e}")


def add_feature_to_document():
    try:
        name = input("Введіть ім'я тварини для додавання характеристики: ")
        new_feature = input("Введіть нову характеристику: ")
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count > 0:
            print(f"Характеристика додана до тварини {name}.")
        else:
            print(f"Тварину з ім'ям {name} не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def delete_document():
    try:
        name = input("Введіть ім'я тварини для видалення: ")
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Тварину з ім'ям {name} видалено.")
        else:
            print(f"Тварину з ім'ям {name} не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def delete_all_documents():
    try:
        confirm = input("Ви дійсно хочете видалити всі документи? (yes/no): ")
        if confirm.lower() == "yes":
            result = collection.delete_many({})
            print(f"Видалено {result.deleted_count} документів.")
        else:
            print("Видалення скасовано.")
    except PyMongoError as e:
        print(f"Помилка при роботі з MongoDB: {e}")


def main():
    while True:
        print("\nДоступні дії:")
        print("1 - Створити запис про тварину")
        print("2 - Показати всі записи")
        print("3 - Пошук запису за ім'ям тварини")
        print("4 - Оновити вік тварини")
        print("5 - Додати особливість до тварини")
        print("6 - Видалити запис про тварину")
        print("7 - Видалити всі записи")
        print("8 - Вийти")
        choice = input("Виберіть дію: ")

        if choice == "1":
            create_document()
        elif choice == "2":
            read_all_documents()
        elif choice == "3":
            read_document_by_name()
        elif choice == "4":
            update_document_age()
        elif choice == "5":
            add_feature_to_document()
        elif choice == "6":
            delete_document()
        elif choice == "7":
            delete_all_documents()
        elif choice == "8":
            break
        else:
            print("Некоректний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()