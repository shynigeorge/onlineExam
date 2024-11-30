from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('questions/', views.submit_response, name='submit_response'),

    path('results/', views.calculate_credit_score, name='calculate_credit_score'),

]