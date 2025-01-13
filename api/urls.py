from django.urls import path
from . import views


urlpatterns = [ 
    path('login/', views.LoginView.as_view()),
    path('register/', views.UserRegistrationView.as_view()),
    path('passwordreset/', views.ResetPasswordView.as_view()),
    path('forgotpassword/', views.ForgotPasswordView.as_view()),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
]
