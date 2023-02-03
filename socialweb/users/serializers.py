from .models import *
from rest_framework import serializers

# Сериалайзер для пользователя
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model=UserModel
        fields=['pk','username','name', 'surname', 'email', 'date_of_birth','gender',
        'main_photo', 'phone', 'password', 'password2']  
        depth=2
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = UserModel(
            username=self.validated_data['username'], # Назначаем Логин
            name=self.validated_data['name'],
            surname=self.validated_data['surname'],
            email=self.validated_data['email'],
            date_of_birth=self.validated_data['date_of_birth'],
            gender=self.validated_data['gender'],
            country=self.validated_data['country'],
            main_photo=self.validated_data['main_photo'],
            phone=self.validated_data['phone'],
            )

        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя 
        return user
    
    # Этот сериалайзер не доделан, проблема с полем многие ко многим - оно не отображается в форме
class UserFriendsSerializer(serializers.ModelSerializer):
    # #####указываем friends, т.к. оно является many-to-many field, теперь будет отображаться __str__ метод, иначе будут отображаться первичные ключи
    # Ссылаемся на сериализатор пользователя, при отображении в ключе user_friends будут поля из UserSerializer
    user_friends = UserSerializer(many=True, source='friends') 
    class Meta:
        model=UserModel
        fields=['pk','name','surname', 'user_friends']  
        depth=1
    

# Сериалайзер для фото
class PhotoSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    # user = UserSerializer(many=True, read_only=True) 
    # user_name =serializers.ReadOnlyField(source='usermodel.user', read_only=True)
  
    class Meta:
        model=PhotoModel
        fields=['pk','user','photos']  
        
# Сериалайзер для запросов в друзья
class FriendshipRequestSerializer(serializers.ModelSerializer):
    from_user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.HiddenField(default=False)
    def validate(self, data):
        if data['from_user']==data['to_user']:
             raise serializers.ValidationError("Вы не можете предложить дружбу самому себе") 
        return data
    class Meta:
        model=FriendshipRequestModel
        fields=['from_user','to_user','status']  

# Сериалайзер для отклонения запроса в друзья
class FriendshipRejectSerializer(serializers.ModelSerializer):
    from_user=serializers.StringRelatedField(read_only=True) 
    to_user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.HiddenField(default=True)

    class Meta:
        model=FriendshipRequestModel
        fields=['from_user','to_user','status']  


# Сериалайзер для принятия запроса в друзья, не реализовано добавление друга в usermodel
class FriendshipAcceptSerializer(serializers.ModelSerializer):
    from_user=serializers.StringRelatedField(read_only=True) 
    to_user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.HiddenField(default=True)
    # def update(self, instance, validated_data):
    #     user1=UserModel.objects.get(username=self.from_user)
    #     user2=UserModel.objects.get(username=self.to_user)
    #     user1.friends.add(user2)
    #     user2.friends.add(user1)
    

    # def save(self, *args, **kwargs):
    #     # Создаём объект класса User
    #     user = UserModel(
    #         username=self.validated_data['username'], # Назначаем Логин
    #         name=self.validated_data['name'],
    #         surname=self.validated_data['surname'],
    #         email=self.validated_data['email'],
    #         date_of_birth=self.validated_data['date_of_birth'],
    #         gender=self.validated_data['gender'],
    #         country=self.validated_data['country'],
    #         main_photo=self.validated_data['main_photo'],
    #         phone=self.validated_data['phone'],
        
    #         )

    #     # Проверяем на валидность пароль
    #     password = self.validated_data['password']
    #     # Проверяем на валидность повторный пароль
    #     password2 = self.validated_data['password2']
    #     # Проверяем совпадают ли пароли
    #     if password != password2:
    #         # Если нет, то выводим ошибку
    #         raise serializers.ValidationError({password: "Пароль не совпадает"})
    #     # Сохраняем пароль
    #     user.set_password(password)
    #     # Сохраняем пользователя
    #     user.save()
    #     # Возвращаем нового пользователя 
    #     return user

    class Meta:
        model=FriendshipRequestModel
        fields=['from_user','to_user','status']  