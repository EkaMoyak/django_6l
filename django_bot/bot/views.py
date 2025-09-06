from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramUser
from .serializers import TelegramUserSerializer, TelegramUserCreateSerializer


@api_view(['POST'])
def register_user(request):
    """
    Регистрация пользователя через Telegram бот
    Принимает POST-запрос с данными пользователя
    Возвращает JSON-ответ с результатом регистрации
    """
    try:
        # Проверяем, существует ли пользователь
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({
                'success': False,
                'message': 'Не указан ID пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Пытаемся найти существующего пользователя
            user = TelegramUser.objects.get(user_id=user_id)
            serializer = TelegramUserSerializer(user)
            return Response({
                'success': True,
                'message': 'Пользователь уже зарегистрирован',
                'user': serializer.data,
                'existing': True
            }, status=status.HTTP_200_OK)

        except TelegramUser.DoesNotExist:
            # Создаем нового пользователя
            serializer = TelegramUserCreateSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                user_serializer = TelegramUserSerializer(user)
                return Response({
                    'success': True,
                    'message': 'Пользователь успешно зарегистрирован',
                    'user': user_serializer.data,
                    'existing': False
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': 'Неверные данные для регистрации',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'success': False,
            'message': 'Внутренняя ошибка сервера',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def user_list(request):
    """
    Получение списка всех пользователей (для тестирования)
    """
    users = TelegramUser.objects.all()
    serializer = TelegramUserSerializer(users, many=True)
    return Response({
        'success': True,
        'count': users.count(),
        'users': serializer.data
    })


@api_view(['GET'])
def user_detail(request, user_id):
    """
    Получение информации о конкретном пользователе
    """
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        serializer = TelegramUserSerializer(user)
        return Response({
            'success': True,
            'user': serializer.data
        })
    except TelegramUser.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Пользователь не найден'
        }, status=status.HTTP_404_NOT_FOUND)