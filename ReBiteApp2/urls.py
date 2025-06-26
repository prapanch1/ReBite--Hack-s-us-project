from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("book/", views.book, name="book"),
    path("send_otp/", views.send_otp, name='send_otp'),
    path("verify_otp/", views.verify_otp, name='verify_otp'),
    path('login_success/', views.login_success, name='login_success'),
    path('login/', views.login, name='login'),
    path('save_user/', views.save_user, name='save_user'),
    path('add_food/', views.add_food, name='add_food'),

]
