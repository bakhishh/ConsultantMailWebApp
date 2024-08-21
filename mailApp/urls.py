from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_excel, name='display_excel'),
    path('send_to_all_consultant/', views.send_to_all_consultant, name='send_to_all_consultant'),
    path('send_to_consultant/<int:consultant_id>/', views.send_to_consultant, name='send_to_consultant'),
    path('send_to_consultant_and_assistant/<int:consultant_id>/', views.send_to_consultant_and_assistant, name='send_to_consultant_and_assistant'),
    path('send/<int:id>/', views.send_to_one, name='send_to_one'),
]
