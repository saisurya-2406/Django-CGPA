from django.urls import path
from .views import login_page, register_page, custom_logout, cgpa_calculator, edit_subject, delete_subject, result

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register_page, name='register'),
    path('', cgpa_calculator, name='cgpa_calculator'),  # default page after login
    path('edit/<int:subject_id>/', edit_subject, name='edit_subject'),
    path('delete/<int:subject_id>/', delete_subject, name='delete_subject'),
    path('result/', result, name='result'),
]
