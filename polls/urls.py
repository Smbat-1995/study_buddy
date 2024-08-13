from django.urls import path
from polls import views

urlpatterns = [
    
    path('', views.home , name = 'home'),
    path('login/', views.loginView , name = 'login'),
    path('logout/', views.logoutView , name = 'logout'),
    path('register/', views.registerView , name = 'register'),
    path('create-room/', views.create_room , name = 'create-room'),
    path('modify_room/<str:pk>', views.modify_room , name = 'modify_room'),
    path('delete_object/<str:pk>', views.delete_room , name = 'delete_object'),
    path('delete-message/<str:pk>', views.delete_message , name = 'delete-message'),
    path('room/<str:pk>/', views.room , name = 'room'),
    path('user_page/<str:pk>/', views.profileView , name = 'user_page'),
    path('update-user/', views.updateUserView , name = 'update-user'),
    path('topics/', views.topicsView , name = 'topics'),
]