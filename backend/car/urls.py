from django.contrib import admin
from django.urls import path, include
from .views import CarView

urlpatterns = [
    path("cars/", CarView.as_view()),
]
