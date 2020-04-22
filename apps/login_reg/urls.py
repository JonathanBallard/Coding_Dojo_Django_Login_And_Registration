from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.index), 
    path('register/', views.register), 
    path('login/', views.login), 
    path('welcome/', views.welcome), 
    path('destroy/', views.destroy), 
    path('register/ajax/', views.reg_ajax), 

] 
