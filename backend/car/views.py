from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Car, Reservation
from .serializers import CarSerializer, ReservationSerializer
from django.utils import timezone
# Create your views here.


class CarView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        queryset = queryset.filter(is_available=True)
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        cond1 = Q(start_date__lt=end)
        cond2 = Q(end_date__gt=start)

        not_available = Reservation.objects.filter(
            cond1 & cond2).values_list('car_id', flat=True)

        queryset = queryset.exclude(id__in=not_available)

        return queryset


class ReservationListCreateView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == "GET" and not self.request.user.is_staff:
            queryset = queryset.filter(customer=self.request.user)

        return queryset


class ReservationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(customer=self.request.user)
