import requests

'''Регистрация'''
url = "http://localhost:8000/api/v1/user/register/"
data = {
    'username': "nick",
    "email": "a@gmail.com",
    "password": "123",
    "first_name": "Nikita",
    "last_name": "Fomenko",
    "company": "Example Company",
    "position": "Manager",
    "user_type": "buyer"
}
response = requests.post(url, json=data)

print("\n📝 Регистрация пользователя:")
print(f"Статус код: {response.status_code}")
if response.status_code == 201:
    print(f"✅ Пользователь успешно зарегистрирован!")
    user_data = response.json()['user']
    print(f"  Имя: {user_data['first_name']} {user_data['last_name']}")
    print(f"  Логин: {user_data['username']}")
    print(f"  Email: {user_data['email']}")
    print(f"  Компания: {user_data['company']}")
    print(f"  Должность: {user_data['position']}")
    print(f"  Тип пользователя: {user_data['user_type']}")
else:
    print(f"❌ Ошибка: {response.json()}")

'''Вход'''
url = "http://localhost:8000/api/v1/user/login/"
data = {
    'username': 'nick',
    'password': '123'
}
response = requests.post(url, data=data)

print("\n🔑 Вход в систему:")
print(f"Статус код: {response.status_code}")
if response.status_code == 200:
    print(f"✅ Вход выполнен успешно!")
    auth_data = response.json()
    print(f"  Access Token: {auth_data['access']}")
    print(f"  Refresh Token: {auth_data['refresh']}")
    print(f"  Имя пользователя: {auth_data['user']['first_name']} {auth_data['user']['last_name']}")
    print(f"  Компания: {auth_data['user']['company']}")
    print(f"  Тип пользователя: {auth_data['user']['user_type']}")
    access_token = auth_data['access']
    headers = {'Authorization': f'Bearer {access_token}'}
else:
    print(f"❌ Ошибка: {response.json()}")
#
# """Список магазинов"""
# url = 'http://localhost:8000/api/v1/shops/'  # Эндпоинт для получения списка магазинов
# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     shops = response.json()
#     print("🛍️ Список магазинов:")
#     for shop in shops:
#         print(f"ID: {shop['id']}, Название: {shop['name']}, URL: {shop.get('url', 'Не указан')}, Статус: {'Активен' if shop['state'] else 'Неактивен'}")
# else:
#     print(f"❌ Ошибка получения списка магазинов: {response.status_code}, {response.text}")
#
# """Список категорий"""
# url = 'http://localhost:8000/api/v1/categories/'  # Эндпоинт для получения списка категорий
# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     categories = response.json()
#     print("📂 Список категорий:")
#     for category in categories:
#         print(f"ID: {category['id']}, Название: {category['name']}")
# else:
#     print(f"❌ Ошибка получения списка категорий: {response.status_code}, {response.text}")
#
# '''Список товаров'''
# url = 'http://localhost:8000/api/v1/products/'
# response = requests.get(url)
#
# if response.status_code == 200:  # Проверяем успешность запроса
#     products = response.json()
#
#     for product_info in products:
#         product = product_info['product']
#         shop = product_info['shop']
#         parameters = product_info['product_parameters']
#
#         print(f"Название продукта: {product['name']}")
#         print(f"Категория: {product['category']}")
#         print(f"Магазин: {shop['name']} (Состояние: {'Активен' if shop['state'] else 'Неактивен'})")
#         print(f"Количество: {product_info['quantity']}")
#         print(f"Цена: {product_info['price']} руб.")
#         print(f"РРЦ: {product_info['price_rrc']} руб.")
#         print("Параметры:")
#         for param in parameters:
#             print(f"  - {param['parameter']}: {param['value']}")
#         print("-" * 40)  # Разделитель между продуктами
# else:
#     print(f"Не удалось получить данные. Код ответа: {response.status_code}")
#
# '''Проверка пустой корзины'''
# basket_url = 'http://localhost:8000/api/v1/basket/'
# response = requests.get(basket_url, headers=headers)
# print("Пустая корзина:", response.json())
#
# """Добавление товара"""
# add_item_url = 'http://localhost:8000/api/v1/basket/'
# item_data = {
#         'product_info_id': 1, 'quantity': 1,
#     }  # ID товара и количество
# response = requests.post(add_item_url, json=item_data, headers=headers)
# if response.status_code == 201:  # Код успешного добавления
#     print(f"✅ Товар успешно добавлен в корзину: {response.json()['ordered_items'][0]['product_info']['product']['name']}")
#     print(f"ID корзины: {response.json()['id']}, Статус: {response.json()['status']}")
# else:
#     print(f"❌ Ошибка при добавлении товара: {response.status_code}, {response.text}")
#
# """Проверка обновленной корзины"""
# basket_url = 'http://localhost:8000/api/v1/basket/'
# response = requests.get(basket_url, headers=headers)
#
# if response.status_code == 200:  # Успешный запрос
#     basket = response.json()
#     print("\n🛒 Корзина:")
#     print(f"ID: {basket['id']}, Статус: {basket['status']}, Дата: {basket['dt']}")
#     print(f"Общая сумма: {basket['total_sum']} руб.")
#     print("Содержимое корзины:")
#     for item in basket['ordered_items']:
#         product_info = item['product_info']
#         print(f"  - Товар: {product_info['product']['name']}")
#         print(f"    Категория: {product_info['product']['category']}")
#         print(f"    Магазин: {product_info['shop']['name']}")
#         print(f"    Цена: {product_info['price']} руб., РРЦ: {product_info['price_rrc']} руб.")
#         print(f"    Количество: {item['quantity']}, Сумма: {item['total_price']} руб.")
#         print("    Параметры:")
#         for param in product_info['product_parameters']:
#             print(f"      • {param['parameter']}: {param['value']}")
#         print("-" * 40)
# else:
#     print(f"❌ Ошибка получения корзины: {response.status_code}, {response.text}")
#
# '''Обновление корзины'''
# basket_data = response.json()
# first_item_id = basket_data['ordered_items'][0]['id']
# update_url = f'http://localhost:8000/api/v1/basket/{first_item_id}/'
# update_data = {'quantity': 2}
# response = requests.put(update_url, json=update_data, headers=headers)
# if response.status_code != 200:
#     print(f"❌ Ошибка обновления количества: {response.status_code}, {response.text}")
# else:
#     updated_item = response.json()
#     product_name = updated_item['product_info']['product']['name']
#     quantity = updated_item['quantity']
#     total_price = updated_item['total_price']
#     print(f"✅ Количество обновлено:")
#     print(f"Товар: {product_name}")
#     print(f"Количество: {quantity}")
#     print(f"Итоговая сумма: {total_price} руб.")
#
# '''Удаление товара'''
# basket_data = response.json()
# update_url = f'http://localhost:8000/api/v1/basket/{first_item_id}/'
# response = requests.delete(update_url, headers=headers)
#
# if response.status_code != 204:
#     print("Ошибка удаления товара:", response.text)
# else:
#     print("Товар успешно удалён")
#
#
# """Создание контакта"""
# url = 'http://localhost:8000/api/v1/contacts/'
# data = {
#     "type": "phone",
#     "value": "+71234567890"
# }
# response = requests.post(url, json=data, headers=headers)
# if response.status_code == 201:
#     print("Контакт успешно создан:", response.json())
# else:
#     print(f"Ошибка: {response.status_code}, {response.text}")
#
# """Получение контакта"""
# url = 'http://localhost:8000/api/v1/contacts/'
# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     contacts = response.json()
#     for contact in contacts:
#         print(f"ID: {contact['id']}, Тип: {contact['type']}, Значение: {contact['value']}")
# else:
#     print(f"Ошибка: {response.status_code}, {response.text}")
#
# """Обновление контакта"""
# url = 'http://localhost:8000/api/v1/contacts/'
# data = {
#     "id": 1,  # ID контакта, который нужно обновить
#     "value": "+79998887766"
# }
# response = requests.put(url, json=data, headers=headers)
# if response.status_code == 200:
#     print("Контакт успешно обновлён:", response.json())
# else:
#     print(f"Ошибка: {response.status_code}, {response.text}")
#
# """Получение контакта"""
# url = 'http://localhost:8000/api/v1/contacts/'
# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     contacts = response.json()
#     for contact in contacts:
#         print(f"ID: {contact['id']}, Тип: {contact['type']}, Значение: {contact['value']}")
# else:
#     print(f"Ошибка: {response.status_code}, {response.text}")
#
# """Удаление контакта"""
# url = 'http://localhost:8000/api/v1/contacts/'
# data = {"ids": "1"}  # IDs контактов, которые нужно удалить
# response = requests.delete(url, json=data, headers=headers)
#
# if response.status_code == 200:
#     print("Контакты успешно удалены:", response.json())
# else:
#     print(f"Ошибка: {response.status_code}, {response.text}")
#
"""Создание контакта"""
url = 'http://localhost:8000/api/v1/contacts/'
data = {
    "type": "phone",
    "value": "+71234567890"
}
response = requests.post(url, json=data, headers=headers)
if response.status_code == 201:
    print("Контакт успешно создан:", response.json())
else:
    print(f"Ошибка: {response.status_code}, {response.text}")
#
# '''Просмотр профиля'''
# url = 'http://localhost:8000/api/v1/user/profile/'
# response = requests.get(url, headers=headers)
# print("Информация о пользователе:", response.json())


"""Добавление товара"""
add_item_url = 'http://localhost:8000/api/v1/basket/'
item_data = {
    'product_info_id': 2,  # ID товара
    'quantity': 1,  # Количество товара
}
response = requests.post(add_item_url, json=item_data, headers=headers)

if response.status_code == 201:  # Успешное добавление
    basket = response.json()
    ordered_items = basket.get('ordered_items', [])

    # Проверяем наличие второго товара
    if len(ordered_items) > 1:
        second_item_name = ordered_items[1]['product_info']['product']['name']
        print(f"✅ Второй товар в корзине: {second_item_name}")
    else:
        print("❌ В корзине недостаточно товаров для вывода второго элемента.")

    print(f"ID корзины: {basket['id']}, Статус: {basket['status']}")
else:
    print(f"❌ Ошибка при добавлении товара: {response.status_code}, {response.text}")


"""Добавление товара"""
add_item_url = 'http://localhost:8000/api/v1/basket/'
item_data = {
    'product_info_id': 3,  # ID товара
    'quantity': 1,  # Количество товара
}
response = requests.post(add_item_url, json=item_data, headers=headers)

if response.status_code == 201:  # Успешное добавление
    basket = response.json()
    ordered_items = basket.get('ordered_items', [])

    # Проверяем наличие второго товара
    if len(ordered_items) > 1:
        second_item_name = ordered_items[1]['product_info']['product']['name']
        print(f"✅ Второй товар в корзине: {second_item_name}")
    else:
        print("❌ В корзине недостаточно товаров для вывода второго элемента.")

    print(f"ID корзины: {basket['id']}, Статус: {basket['status']}")
else:
    print(f"❌ Ошибка при добавлении товара: {response.status_code}, {response.text}")

"""Подтверждение заказа"""
url = 'http://localhost:8000/api/v1/orders/confirm/'  # Эндпоинт подтверждения заказа
data = {
    "basket_id": 1,  # ID корзины
    "contact_id": 2    # ID контакта
}
response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    print("Заказ успешно подтвержден:", response.json())
else:
    print(f"Ошибка подтверждения заказа: {response.status_code}, {response.text}")

"""Список заказа"""
url = 'http://localhost:8000/api/v1/orders/'  # Эндпоинт получения заказов
response = requests.get(url, headers=headers)
if response.status_code == 200:
    orders = response.json()
    for order in orders:
        print(f"Номер заказа: {order['id']}, Статус: {order['status']}, Сумма: {order.get('total_sum', 'N/A')}")
        print("Позиции в заказе:")
        for item in order.get('ordered_items', []):
            print(f"  - Товар: {item['product_info']['product']['name']}, Количество: {item['quantity']}, Сумма: {item['total_price']}")
        print("-" * 40)
else:
    print(f"Ошибка получения списка заказов: {response.status_code}, {response.text}")