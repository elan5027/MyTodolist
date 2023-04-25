from django.urls import path
from todolist import views

urlpatterns = [
    path('', views.TodosAPIView.as_view()),
    path('<int:pk>/', views.TodoAPIView.as_view()),
    path('done/<int:pk>/', views.DoneTodoAPIView.as_view()),
]