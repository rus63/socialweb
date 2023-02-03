from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView 
from .models import UserModel, PhotoModel, FriendshipRequestModel
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView  
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .forms import RegisterUserForm, AddPhotoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View
import logging

logger=logging.getLogger('main')
# Create your views here.

    
class RegisterUser(CreateView):
    form_class = RegisterUserForm    
    template_name='users/register.html'
    
    def get_success_url(self):
        logger.info('User has been registred')
        return reverse_lazy('home')
    

class LoginUser(LoginView):
    form_class = AuthenticationForm
    
    template_name='users/login.html'
    
   

class MypageView(DetailView):
    template_name='users/mypage.html'
    model=UserModel
    queryset = UserModel.objects.filter()
    context_object_name = 'mypage'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cnt=FriendshipRequestModel.objects.filter(to_user=self.request.user, status=False)
            if len(cnt)>0:  
                context['countfriends']=f'(+{len(cnt)})'
        logger.info('User has got mypage')
        return context
    


# Представления для друзей

class FriendsView(DetailView):
    model=UserModel
    template_name='users/friends.html'
    context_object_name = 'friend'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['userfriends']=UserModel.objects.get(pk=self.kwargs['pk'])
        context['friendsrequests']=FriendshipRequestModel.objects.filter(to_user=self.request.user, status=False)
        if len(context['friendsrequests'])>0:
            context['zapros']='Запросы в друзья:'

        context['myfriends']=UserModel.objects.filter(pk=self.request.user.pk)
        context['allusers']=UserModel.objects.all().exclude(username='admin').order_by('name','surname')
        
        cnt=UserModel.objects.get(pk=self.request.user.pk)
        if len(cnt.friends.all())==0:
            context['nofriends']='У вас пока нет друзей'
        if self.request.user.is_authenticated:
            cnt=FriendshipRequestModel.objects.filter(to_user=self.request.user, status=False)
            if len(cnt)>0:  
                context['countfriends']=f'(+{len(cnt)})'
        logger.info('Data about friends has been accepted')

        return context
 
# Отправление предложения дружбы
class FriendsSendRequestView(LoginRequiredMixin, CreateView):
    model=FriendshipRequestModel
    fields='__all__'
    template_name= 'users/friendssendrequest.html'
    
    def post(self, request, *args, **kwargs):
       from_user=request.user
       to_user=UserModel.objects.get(pk=kwargs['pk'])
       frequest=FriendshipRequestModel.objects.get_or_create(from_user=from_user, to_user=to_user, status=False)
       return redirect(reverse_lazy('successfrequest'))
  

# def send_request(request, pk):
#   from_user=request.user
#   to_user=UserModel.objects.get(pk=pk)
#   frequest=FriendshipRequestModel.objects.get_or_create(from_user=from_user, to_user=to_user, status=False)
#   return redirect(reverse_lazy('successfrequest'))


def SuccessFrequest(request):
    return render(request, 'users/successfrequest.html')


# Удаление друга
class FriendsDeleteView(LoginRequiredMixin,DeleteView):
    model=UserModel
    template_name='users/deletefriends.html'
    # success_url=reverse_lazy('friendship')

    def post(self, request, *args, **kwargs): 
        user1=request.user
        user2=UserModel.objects.get(pk=kwargs['pk'])
        user1.friends.remove(user2)    
        user2.friends.remove(user1)
        return redirect(reverse_lazy('friendship', kwargs={'pk':request.user.pk}))
        
# def remove_friend(request, pk):
    
#     user1=request.user
#     user2=UserModel.objects.get(pk=pk)
#     user1.friends.remove(user2)    
#     user2.friends.remove(user1)
#     return HttpResponse('<h1>Пользователь удален из списка друзей</h1>')


# Принятие предложения дружбы
class FriendsRequestAcceptView(DetailView):
    model=FriendshipRequestModel
    template_name='users/successaccept.html'
    
    def get(self, request, *args, **kwargs):
        frequest=FriendshipRequestModel.objects.get(pk=kwargs['pk'])
        user1=request.user
        user2=frequest.from_user
        user1.friends.add(user2)    
        user2.friends.add(user1)
        frequestupd=FriendshipRequestModel.objects.filter(pk=kwargs['pk']).update(status=True)
        return super().get(self, request, *args, **kwargs)


# def accept_request(request, pk):
#     frequest=FriendshipRequestModel.objects.get(pk=pk)
#     user1=request.user
#     user2=frequest.from_user
#     user1.friends.add(user2)    
#     user2.friends.add(user1)
#     frequestupd=FriendshipRequestModel.objects.filter(pk=pk).update(status=True)
#     return HttpResponse('<h1>Пользователь добавлен</h1>')


# Отклонение дружбы
class FriendsRejectView(DetailView):
    model=FriendshipRequestModel
    template_name= 'users/friendsreject.html'
    
    def get(self, request, *args, **kwargs):
       from_user=UserModel.objects.get(pk=kwargs['pk'])
       to_user=self.request.user
       frequest=FriendshipRequestModel.objects.filter(from_user=from_user, to_user=to_user).update(status=True)
       return redirect(reverse_lazy('friendship', kwargs={'pk':request.user.pk}))

# Предаставления для фотографий

class PhotoPostView(CreateView):
    form_class = AddPhotoForm
    template_name = 'users/photopost.html'
    def get_success_url(self):
        return reverse_lazy('successpost')
        
    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        
        return super(PhotoPostView, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['images']=PhotoModel.objects.filter(user=self.request.user)
        # print(len(context['images']))
        if len(context['images'])==0:
            context['noimage']='У вас пока нет фотографий'
        if self.request.user.is_authenticated:
            cnt=FriendshipRequestModel.objects.filter(to_user=self.request.user, status=False)
            if len(cnt)>0:  
                context['countfriends']=f'(+{len(cnt)})'
        return context

def SuccessPost(request):
    return render(request, 'users/successpost.html')



class DeletePhotoPostView(LoginRequiredMixin, DeleteView):
    model=PhotoModel
    template_name='users/deletephotopost.html'
    success_url=reverse_lazy('successdeletepost')
    
    def post(self, request, *args, **kwargs): 
        obj = PhotoModel.objects.get(pk=kwargs['pk'])
        if request.user == obj.user:
            obj.delete()        
            return HttpResponseRedirect(self.success_url)

        else:
           return HttpResponse('Нельзя удалять')  
        
        

    # def post(self, request, *args, **kwargs):
    #     object_instance=self.get_object()
    #     object_user=object_instance.user
        
    #     if request.user.pk==request.get_object().user.pk:
    #         return super().post(request, *args, **kwargs)
    #     return reverse_lazy('home')

    
    # permissions=[IsAuthor,]
def del_post(request, **kwargs):
  object = PhotoModel.objects.get(pk=kwargs['pk'])
  if request.user == object.user:
    object.delete()
    return redirect('/')

  else:
    return HttpResponse('Nonono!')


def SuccessDeletePost(request):
    return render(request, 'users/successdeletepost.html')



class HomeView(ListView):
    template_name='users/base.html'
    model=UserModel
    extra_context={'title':'Главная страница'}


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            cnt=FriendshipRequestModel.objects.filter(to_user=self.request.user, status=False)
            if len(cnt)>0:  
                context['countfriends']=f'(+{len(cnt)})'
        return context
        
            




