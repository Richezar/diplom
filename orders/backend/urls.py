from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ShopView, CategoryView, UnifiedRegisterView, UserProfileView, ProductInfoView,
    LoginAccountView, BasketView, ContactView, ConfirmOrderView, ListOrdersView, BasketItemView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', UnifiedRegisterView.as_view()),  # Объединённая регистрация с email
    path('user/login/', LoginAccountView.as_view()),        # Вход
    path('user/profile/', UserProfileView.as_view()),       # Профиль
    path('shops/', ShopView.as_view()),                     # Список магазинов
    path('categories/', CategoryView.as_view()),            # Категории
    path('products/', ProductInfoView.as_view()),           # Продукты
    path('basket/', BasketView.as_view()),                  # Корзина
    path('basket/<int:id>/', BasketItemView.as_view()),     # Отдельная позиция корзины
    path('contacts/', ContactView.as_view()),               # Контакты
    path('orders/confirm/', ConfirmOrderView.as_view()),    # Подтверждение заказа
    path('orders/', ListOrdersView.as_view()),              # Список заказов
]
