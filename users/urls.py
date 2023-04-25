from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('user/', views.UserView.as_view()),
]