
from django.urls import path
from Accounts import views
urlpatterns = [
    path('registerpage/',views.registerpage,name='registerpage'),
    path('loginpage/',views.login,name='loginpage'),
    path('account_settings/',views.account_setting,name='account_settings'),
    path('logout/',views.logout,name='logoutpage'),
]
