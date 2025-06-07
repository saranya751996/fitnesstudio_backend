from django.shortcuts import render

from rest_framework.decorators import api_view
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from rest_framework import serializers
from .serializers import FitnessClassListSerializer, BookingSerializer, BookingDetailsSerializer
from django.shortcuts import get_object_or_404
# from core.base import SoftDelete
from rest_framework import viewsets, mixins
from django.http import JsonResponse
from core.mixins import ResponseViewMixin


class FitnessClassView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet, ResponseViewMixin):

    serializer_class = FitnessClassListSerializer
    queryset = FitnessClass.objects.all()

    def list(self, request, **kwargs):
        try:

            queryset = self.get_queryset()
            serializer = FitnessClassListSerializer(queryset, many=True)
            return self.jp_response(s_code='HTTP_200_OK', data=serializer.data)
        except Exception as e:
            return self.jp_error_response('HTTP_500_INTERNAL_SERVER_ERROR', 'EXCEPTION', [str(e), ])

    def post(self, request, *args, **kwargs):
        try:
            serializer = BookingSerializer(
                data=request.data, context={'request': request})
            if not serializer.is_valid():
                return self.jp_error_response('HTTP_400_BAD_REQUEST', self.error_msg_list(serializer.errors))
            serializer.save()
            return self.jp_response(s_code='HTTP_201_CREATED', data={'booking-details': serializer.data})
        except Exception as e:
            return self.jp_error_response('HTTP_500_INTERNAL_SERVER_ERROR', 'EXCEPTION', [str(e), ])


class BookingView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet, ResponseViewMixin):
    serializer_class = BookingDetailsSerializer
    queryset = Booking.objects.all()

    def client_bookings(self, request, *args, **kwargs):
        try:
            client_email = self.request.query_params.get('client_email')
            if not client_email.strip():
                return self.jp_error_response('HTTP_403_FORBIDDEN', 'Please enter an email id')
            if not Booking.objects.filter(client_email=client_email).exists():
                return self.jp_error_response(
                    "HTTP_404_NOT_FOUND",
                    "EXCEPTION",
                    "No booking available for the email",
                )

            self.queryset = self.get_queryset().filter(
                client_email=client_email)
            data = super().list(self, request, *args, **kwargs).data  # listing with pagination

            return self.jp_response(s_code='HTTP_200_OK', data=data)

        except Exception as e:
            return self.jp_error_response('HTTP_500_INTERNAL_SERVER_ERROR', 'EXCEPTION', [str(e), ])
