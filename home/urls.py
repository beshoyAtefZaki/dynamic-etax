from django.urls import path
from .views import*

urlpatterns = [
    path('' , home , name='home') ,
      path ('login/' , user_login , name ='login') ,
    path ('import_reciever/' , import_reciever , name ='import_reciever') ,
    path('logout/' , logout_view , name ='logout' ) ,
    path('create-user' ,  register_view ,name= 'creat-user') ,
    path('user_list' ,  user_list ,name= 'user_list'),
    path('delete_user/<id>' ,  delete_user ,name= 'delete_user') ,
    path('update_user/<id>' ,  update_user ,name= 'update_user') ,
    path('reciever_list' ,  reciever_list ,name= 'reciever_list') ,
    path('creat_receiver' ,  creat_receiver ,name= 'creat_receiver') ,
    path('delete_receiver/<id>' ,  delete_receiver ,name= 'delete_receiver') ,
    path('edit_receiver/<id>' ,  edit_receiver ,name= 'edit_receiver') ,
    path ('errolog_list/' , errolog_list , name ='errolog_list') ,]