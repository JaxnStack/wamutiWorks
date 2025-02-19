from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-questions/', views.upload_questions, name='upload_questions'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
]
