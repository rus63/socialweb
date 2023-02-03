from rest_framework import generics
from .models import *
from .serializers import UserSerializer, UserFriendsSerializer, PhotoSerializer, FriendshipRequestSerializer, FriendshipRejectSerializer, FriendshipAcceptSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOnlyUserOrReadOnly, IsOnlyUserPhotoOrReadOnly, IsOnlyTo_User



# Представление для отображения или создания пользователя
class UserList(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else: # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)


# Представление для отображения или изменения пользователя(изменение доступно только самому пользователю)
class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsOnlyUserOrReadOnly]

# Представление для удаления пользователя(доступно только самому пользователю)
class UserDestroy(generics.RetrieveDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsOnlyUserOrReadOnly]


# Представление для отображения друзей пользователя(доступно только авторизованным пользователям)
# Представление работает, однако не работает добавление и удаление друзей
class UserFriends(generics.RetrieveUpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserFriendsSerializer
    permission_classes=[IsOnlyUserOrReadOnly]

    def create(self, request, *args, **kwargs):
        data=request.data
        friend=UserModel.object.get(pk=kwargs['pk'])
        for i in data['friends']:
            friends_obj=UserModel.objects.get(pk=request.user.pk)
            friend.friends_obj.add()

    def get_object(self):
        return UserModel.objects.get(pk=self.kwargs.get('pk'))
    

from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins


# Представление для отображения фотографий по первичному ключу, изменять и удалять модет только пользователь

class UserPhotosUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhotoModel.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsOnlyUserPhotoOrReadOnly]
    # authentication_classes=[SessionAuthentication]


# Представление для добавления фотографий, только для авторизованных пользователей

class UserPhotosCreate(generics.CreateAPIView):
    queryset = PhotoModel.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
  


# Представление для создания запросов в друзья
class FriendshipRequest(generics.CreateAPIView):
    queryset = FriendshipRequestModel.objects.all()
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated]


# Представление для отклонения запросов в друзья
class FriendshipReject(generics.RetrieveUpdateAPIView):
    queryset = FriendshipRequestModel.objects.filter(status=False)
    serializer_class = FriendshipRejectSerializer
    permission_classes = [IsOnlyTo_User]

# Представление для принятия запросов в друзья( не реализовано добавление друга usermodel.friends)
class FriendshipAccept(generics.RetrieveUpdateAPIView):
    queryset = FriendshipRequestModel.objects.filter(status=False)
    serializer_class = FriendshipAcceptSerializer
    permission_classes = [IsOnlyTo_User]

    def update(self, request, validated_data, *args, **kwargs):
        instance=UserModel.get_object(pk=request.user.pk)
        instance.friends.add(validated_data['name'])
        instance.save() 