from rest_framework import serializers
from .models import FitnessClass, Booking
from django.core.validators import validate_email


class FitnessClassListSerializer(serializers.ModelSerializer):

    class Meta:

        model = FitnessClass
        fields = ('name', 'date', 'instructor', 'available_slots')


class BookingSerializer(serializers.ModelSerializer):

    fitness_class_id = serializers.CharField(write_only=True,
                                             required=True,
                                             allow_null=False, allow_blank=False)
    client_name = serializers.CharField(
        write_only=True, required=True, allow_blank=False)
    # email format and null value validation checking
    client_email = serializers.EmailField(
        write_only=True, required=True, allow_blank=False)

    def validate(self, validated_data):
        fitness_class = FitnessClass.objects.get(
            id=validated_data['fitness_class_id'])
        booking = Booking.objects.filter(
            client_email=validated_data['client_email'], fitness_class_id=validated_data['fitness_class_id'], is_completed=False).exists()

        if booking:  # check if class already booked in the given email id
            raise serializers.ValidationError(
                "Fitness Class already booked for the given email id")

        if fitness_class.available_slots <= 0:  # check if slot available for the class
            raise serializers.ValidationError(
                "No slots Available for Booking")

        return validated_data

    def create(self, *args, **kwargs):

        try:

            request = self.context["request"]
            booking_data = {
                "client_name": request.data["client_name"],
                "client_email": request.data["client_email"],
                "fitness_class_id": request.data["fitness_class_id"],
            }

            booking = Booking.objects.create(**booking_data)
            fitness_class = FitnessClass.objects.get(
                id=request.data["fitness_class_id"])
            fitness_class.available_slots = fitness_class.available_slots-1
            fitness_class.save()
            return booking

        except Exception as e:
            raise e

    class Meta:
        model = Booking
        fields = '__all__'


class BookingDetailsSerializer(serializers.ModelSerializer):

    fitness_class = FitnessClassListSerializer()

    class Meta:

        model = Booking
        fields = ('client_name', 'client_email', 'fitness_class')
