from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('expense_summary/', views.expense_summary, name='expense_summary'),
     path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]
