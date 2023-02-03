from .models import UserModel, PhotoModel,FriendshipRequestModel
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
# class RegisterUserForm(UserCreationForm):
#     class Meta:
#         model = UserModel
#         fields = '__all__'

class RegisterUserForm(UserCreationForm):
     class Meta:
         model = UserModel
         fields = ['username','name', 'surname', 'email', 'date_of_birth', 'gender', 'country', 'about_me', 'main_photo', 'phone']

class AddPhotoForm(forms.ModelForm):
    class Meta:
         model = PhotoModel
         fields = ['photos']



class AddFriendForm(forms.ModelForm):
    class Meta:
         model = FriendshipRequestModel
         fields = ['status']
# class AddImageForm(forms.ModelForm):
#     class Meta:
#          model = UserModel
#          fields = ['photoalbum']
# class RegisterUserForm(UserModel):
#     username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

