
from django.urls import path, include
from fitness.views import FitnessClassView, BookingView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'fitness-class', FitnessClassView, 'fitness_class')

urlpatterns = [
    path('', include(router.urls)),
    path('list-client-bookings',
         BookingView.as_view({'get': 'client_bookings'}), name='client-bookings'),

]
