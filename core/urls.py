from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_todo, name='add_todo'),
    path('new/', views.new_todo, name='new_todo'),
    path('done/<int:pk>/', views.toggle_todo, name='toggle_todo'),
    path('display/<int:pk>/', views.display_todo, name='display_todo'),
    path('update/<int:pk>/', views.update_todo, name='update_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
]
