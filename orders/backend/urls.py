from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ShopView, CategoryView, RegisterAccountView, UserProfileView, ProductInfoView, \
    LoginAccountView, BasketView, ContactView, ConfirmOrderView, ListOrdersView, BasketItemView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),),
    path('token/refresh/', TokenRefreshView.as_view(),),
    path('user/register/', RegisterAccountView.as_view()), # Регистрация нового пользователя
    path('user/login/', LoginAccountView.as_view()),  # Вход в систему
    path('user/profile/', UserProfileView.as_view()),  # Информация о пользователе
    path('shops/', ShopView.as_view()),  # Список магазинов
    path('categories/', CategoryView.as_view()),  # Список категорий
    path('products/', ProductInfoView.as_view()),  # Список товаров
    path('basket/', BasketView.as_view()), #Просмотр корзины
    path('basket/<int:id>/', BasketItemView.as_view()),
    path('contacts/', ContactView.as_view()),#Контакты
    path('orders/confirm/', ConfirmOrderView.as_view()),  # Подтверждение заказа
    path('orders/', ListOrdersView.as_view()), # Список всех заказов текущего пользователя
]
