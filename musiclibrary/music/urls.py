from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.SongList.as_view()),
    # path('<int:pk>/', views.SongDetail.as_view()),
    ]    