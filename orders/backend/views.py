from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Shop, Category, ProductInfo, Order, OrderItem, Contact, User
from .serializers import ShopSerializer, CategorySerializer, UserRegisterSerializer, UserProfileSerializer, \
    ProductInfoSerializer, MyTokenObtainPairSerializer, OrderSerializer, OrderItemSerializer, ContactSerializer
from django.utils import timezone
from django.db.models import Sum, F, Q
from django.core.mail import send_mail

# Create your views here.
class LoginAccountView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ShopView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductInfoView(generics.ListAPIView):
    serializer_class = ProductInfoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = ProductInfo.objects.select_related(
            'shop', 'product'
        ).prefetch_related(
            'product_parameters__parameter'
        )

        shop_id = self.request.query_params.get('shop_id')
        category_id = self.request.query_params.get('category_id')

        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        if category_id:
            queryset = queryset.filter(product__category_id=category_id)

        return queryset

class BasketView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_basket(self):
        """Получает или создает корзину с аннотацией общей суммы"""
        basket, created = Order.objects.get_or_create(
            user=self.request.user,
            status=Order.Status.BASKET,
            defaults={'dt': timezone.now()}
        )
        return basket

    def post(self, request, *args, **kwargs):
        basket = self.get_basket()
        serializer = OrderItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            product_info = ProductInfo.objects.select_related('product', 'shop').get(
                id=serializer.validated_data['product_info_id'],
                quantity__gte=serializer.validated_data['quantity']  # Проверка наличия
            )
        except ProductInfo.DoesNotExist:
            return Response(
                {"status": False, "error": "Товар не найден или недостаточно на складе"},
                status=status.HTTP_404_NOT_FOUND
            )

        shop = product_info.shop  # Получаем магазин для данного товара

        order_item, created = OrderItem.objects.get_or_create(
            order=basket,
            product_info=product_info,
            shop=shop,  # Указываем магазин
            defaults={'quantity': serializer.validated_data['quantity']}
        )

        if not created:
            new_quantity = order_item.quantity + serializer.validated_data['quantity']
            if new_quantity > product_info.quantity:
                return Response(
                    {"status": False, "error": "Недостаточно товара на складе"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            order_item.quantity = new_quantity
            order_item.save()

        basket.refresh_from_db()
        serializer = self.get_serializer(basket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BasketItemView(generics.GenericAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__user=self.request.user,
            order__status='basket'
        ).select_related('product_info__product', 'product_info__shop')

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, id=self.kwargs['id'])
        return obj

    def put(self, request, *args, **kwargs):
        order_item = self.get_object()
        product_info = order_item.product_info

        serializer = self.get_serializer(
            order_item,
            data=request.data,
            partial=True,
            context={'product_info': product_info}
        )
        serializer.is_valid(raise_exception=True)

        new_quantity = serializer.validated_data.get('quantity', order_item.quantity)
        if new_quantity > product_info.quantity:
            return Response(
                {"status": False, "error": f"Доступно только {product_info.quantity} шт."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        order_item = self.get_object()
        order_item.delete()
        return Response(
            {"status": True, "message": "Позиция удалена из корзины"},
            status=status.HTTP_204_NO_CONTENT
        )

class ContactView(APIView):
    permission_classes = [IsAuthenticated]

    # Получить список контактов текущего пользователя
    def get(self, request, *args, **kwargs):
        contacts = Contact.objects.filter(user=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    # Создать новый контакт
    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id  # Устанавливаем текущего пользователя
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Контакт успешно создан"}, status=201)
        return Response({"status": False, "errors": serializer.errors}, status=400)

    # Редактировать контакт
    def put(self, request, *args, **kwargs):
        contact_id = request.data.get('id')

        # Проверка типа contact_id
        if not isinstance(contact_id, int) and not str(contact_id).isdigit():
            return Response({"status": False, "errors": "ID контакта обязателен и должен быть числом"}, status=400)

        contact = Contact.objects.filter(id=contact_id, user=request.user).first()
        if not contact:
            return Response({"status": False, "errors": "Контакт не найден"}, status=404)

        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Контакт успешно обновлён"})
        return Response({"status": False, "errors": serializer.errors}, status=400)

    # Удалить контакт
    def delete(self, request, *args, **kwargs):
        contact_ids = request.data.get('ids')
        if not contact_ids:
            return Response({"status": False, "errors": "IDs контактов обязательны"}, status=400)

        ids_list = contact_ids.split(',')
        deleted_count = Contact.objects.filter(Q(user=request.user) & Q(id__in=ids_list)).delete()[0]
        if deleted_count > 0:
            return Response({"status": True, "message": f"Удалено {deleted_count} контакт(ов)"}, status=200)
        return Response({"status": False, "errors": "Контакты не найдены"}, status=404)

class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        basket_id = request.data.get('basket_id')
        contact_id = request.data.get('contact_id')

        if not basket_id or not contact_id:
            return Response(
                {"status": False, "error": "basket_id и contact_id обязательны."},
                status=400
            )

        # Проверка корзины
        try:
            basket = Order.objects.get(id=basket_id, user=request.user, status=Order.Status.BASKET)
        except Order.DoesNotExist:
            return Response(
                {"status": False, "error": "Корзина не найдена или не принадлежит пользователю."},
                status=404
            )

        # Проверка контакта
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response(
                {"status": False, "error": "Контакт не найден или не принадлежит пользователю."},
                status=404
            )

        # Подтверждение заказа
        basket.status = Order.Status.CONFIRMED
        basket.save()

        # Отправляем email пользователю о подтверждении заказа
        send_mail(
            "Подтверждение заказа",
            f"Ваш заказ {basket.id} успешно подтвержден.",
            'noreply@example.com',
            [request.user.email],
        )

        return Response(
            {
                "status": True,
                "message": "Заказ успешно подтвержден.",
                "order_id": basket.id,
                "total_sum": basket.total_sum
            },
            status=200
        )

class ListOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user).order_by('-dt')  # Заказы текущего пользователя
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class UnifiedRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            send_mail(
                subject="Подтверждение регистрации",
                message="Вы успешно зарегистрировались!",
                from_email="noreply@example.com",
                recipient_list=[user.email],
            )

            return Response({
                "status": True,
                "message": "Пользователь создан. Подтверждение отправлено на email.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)