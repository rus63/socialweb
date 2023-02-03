from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, AbstractUser
from django_countries.fields import CountryField
import datetime
from django.urls import reverse
# Create your models here.


class UserModel(AbstractUser):
    first_name=None
    last_name=None
    name=models.CharField(max_length=30, verbose_name='Имя')
    surname=models.CharField(max_length=30, verbose_name='Фамилия')
    email=models.EmailField(verbose_name='Адрес электронной почты', max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True )
    main_photo=models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Аватар', null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    
    GENDER = (
            ('M', 'Мужской'),
            ('Ж', 'Женский'),
        )

    gender=models.CharField(max_length=1, choices=GENDER, verbose_name='Пол')
    country=CountryField(verbose_name='Страна')
    date_of_creation=models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации' )
    date_of_online=models.DateTimeField(auto_now=True, verbose_name='Дата последнего выхода в сеть')
    about_me=models.TextField(max_length=500, verbose_name='Информация о себе', blank=True)
    phone=models.CharField(max_length=15, verbose_name='Телефон', blank=True)
    friends=models.ManyToManyField('self', verbose_name='Друзья', blank=True)

    def __str__(self):
        return f'Пользователь @{self.username} {self.name} {self.surname}'

    class Meta:
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'
    

    def get_absolute_url(self):
        return reverse('mypage', kwargs={'pk': self.pk})
    
    def calculate_age(self):
        from datetime import date
        today = date.today()
        try:
            birthday = self.date_of_birth.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.date_of_birth.replace(year=today.year, month=self.date_of_birth.month+1, day=1)
        if birthday > today:
            return today.year - self.date_of_birth.year - 1
        else:
            return today.year - self.date_of_birth.year
    

class PhotoModel(models.Model):
    user=models.ForeignKey('Usermodel', on_delete=models.DO_NOTHING, verbose_name='Альбом пользователя',related_name='user')
    photos=models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение')
    def __str__(self):
        return f'Фотография пользователя {self.user}'

    class Meta:
        verbose_name='Фотография'
        verbose_name_plural='Фотографии'
    def get_absolute_url(self):
        return reverse('photopost', kwargs={'pk': self.pk})


class FriendshipRequestModel(models.Model):
    from_user=models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='От кого',related_name='from_user')
    to_user=models.ForeignKey('UserModel',on_delete=models.CASCADE, verbose_name='Кому', related_name='to_user')  
    status=models.BooleanField(verbose_name='Статус', default=False)
    def __str__(self):
        return f'Запрос от {self.from_user}'

    class Meta:
        verbose_name='Запрос на дружбу'
        verbose_name_plural='Запросы на дружбу'

    
    def get_absolute_url(self):
        return reverse('friendshiprequest', kwargs={'pk': self.pk})

# 

# class Message(models.Model):
#     user1=models.ForeignKey('UserModel', on_delete=models.DO_NOTHING, blank=True, verbose_name='Участник 1', related_name='User1')
#     chat=models.ForeignKey('Chat', on_delete=models.DO_NOTHING, verbose_name='Чат')
#     datetime=models.DateTimeField(auto_now_add=True, verbose_name='Дата/время публикации')
#     content=models.TextField(max_length=300, verbose_name='Реплика', blank=True)
#     photo=models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение', null=True, blank=True)
#     def __str__(self):
#         return f'Сообщение от {self.user1}'

#     class Meta:
#         verbose_name='Сообщение'
#         verbose_name_plural='Сообщения'


# class Chat(models.Model):
#     members=models.ManyToManyField('UserModel', verbose_name='Участники', blank=True)
# # class DialogModel(models.Model):
# #     title=models.CharField(max_length=15, verbose_name='Диалог')
# #     replica=models.ManyToManyField(ReplicaModel, blank=True, verbose_name='реплика 1')

# #     def __str__(self):
# #         return f'Диалог № {self.pk}'

# #     class Meta:
# #         verbose_name='Диалог'
# #         verbose_name_plural='Диалоги'   
# #         order_with_respect_to = 'replica'