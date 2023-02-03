# Django imports
from django.urls import path
from .views import (HomeView, MypageView, LoginUser, RegisterUser,PhotoPostView, 
FriendsView,FriendsRejectView,FriendsSendRequestView, FriendsDeleteView, FriendsRequestAcceptView,
SuccessFrequest,SuccessPost, SuccessDeletePost, DeletePhotoPostView)
from django.contrib.auth.views import LogoutView

# DRF imports
from .api import *
from django.urls import include
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('user/<int:pk>', MypageView.as_view(), name='mypage'),
# Авторизация и регистрация
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

# Фото и действия с ними
    path('postphoto/<int:pk>', PhotoPostView.as_view(), name='photopost'),
    path('successpost/', SuccessPost, name='successpost'),
    path('deletephotopost/<int:pk>', DeletePhotoPostView.as_view(), name='deletephotopost'),
    path('successdeletepost/', SuccessFrequest, name='successfrequest'),
 
# Друзья и действия с ними
    path('friendship/<int:pk>', FriendsView.as_view(), name='friendship'),
    path('successfrequest/', SuccessDeletePost, name='successdeletepost'),
    path('sendrequest/<int:pk>/', FriendsSendRequestView.as_view(), name='sendrequest'),
    path('acceptrequest/<int:pk>/', FriendsRequestAcceptView.as_view(), name='acceptrequest'),
    path('rejectrequest/<int:pk>/', FriendsRejectView.as_view(), name='rejectrequest'),
    path('removefriend/<int:pk>/', FriendsDeleteView.as_view(), name='removefriend'),
    
# DFR маршруты
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/user', UserList.as_view()),
    path('api/v1/user/<int:pk>', UserDetail.as_view()),
    path('api/v1/userdelete/<int:pk>', UserDestroy.as_view()),
    path('api/v1/userfriends/<int:pk>', UserFriends.as_view()),
    path('api/v1/userphotosupdate/<int:pk>', UserPhotosUpdate.as_view()),
    path('api/v1/userphotoscreate/', UserPhotosCreate.as_view()),
    path('api/v1/friendshiprequest/', FriendshipRequest.as_view()),
    path('api/v1/friendshipreject/<int:pk>', FriendshipReject.as_view()),
    path('api/v1/friendshipaccept/<int:pk>', FriendshipAccept.as_view()),
    




    



   
]