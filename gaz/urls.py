from django.urls import path, include
from .views import (
    gaz,
)

urlpatterns = [
    path('gaz/list/', views = gaz.gaz_list, name='gaz_list'),
    path('gaz/create/', views = gaz.create_gaz, name='create_gaz'),
    path('gaz/update/<str:pk>/', views = gaz.update_gaz, name='update_gaz'),
    path('gaz/delete/<str:pk>/', views= gaz.delete_gaz, name='delete_gaz'),

]
