from django.urls import path
from . import views

urlpatterns = [
    path("customer/<str:pk>", views.customer, name="customer"),
    path("register/", views.register, name="register"),
    path("login/", views.loginPage, name="login"),

    path("logout/", views.logoutUser, name="logout"),
    path("", views.home, name="home"),

    path("products/", views.products, name="products"),
    path("user/", views.userPage, name="user-page"),
    

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),
] 