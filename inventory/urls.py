from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:pk>/', views.edit_equipment, name='edit_equipment'),
    path('delete/<int:pk>/', views.delete_equipment, name='delete_equipment'),
    path('', views.home, name='home'),
    path('add/', views.add_equipment, name='add_equipment'),
    path('register/', views.register_user, name='register_user'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
