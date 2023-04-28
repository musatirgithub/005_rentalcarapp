from django.contrib import admin
from django.urls import path, include
from .views import CarView, ReservationListCreateView, ReservationRetrieveUpdateDestroyView

urlpatterns = [
    path("cars/", CarView.as_view()),
    path("reservations/", ReservationListCreateView.as_view()),
    path("reservations/<int:pk>", ReservationRetrieveUpdateDestroyView.as_view()),
]
