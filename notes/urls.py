from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('upload/', views.upload_note, name='upload_note'),
    path('download/<int:note_id>/', views.download_note, name='download_note'),
    path('like/<int:note_id>/', views.like_note, name='like_note'),
    #path('register/', views.register, name='register'),
    path('register/', register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
