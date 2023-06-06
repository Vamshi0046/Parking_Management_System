from django.contrib import admin
from django.urls import path,include
from parking_app import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('addvehcile/',views.addvehicle,name='addvehcile'),
    path('receipt/<int:pk>/', views.receipt, name='receipt'),
    path('addcat/',views.addcat,name='addcat'),
    path('update_status_cat/<int:id>/', views.update_status_cat, name='update_status_cat'),
    path('search/',views.searchbar,name='search'),
    path('manage/',views.manage,name='manage'),
    path('reports/',views.reports,name='reports'),
    path('update_status/<int:id>/', views.update_status, name='update_status'),
    path('update_category/<int:id>/',views.update_category,name="update_category"),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
]
