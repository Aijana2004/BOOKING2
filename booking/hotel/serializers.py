
from rest_framework import serializers
from .models import *


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class HotelListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_name','country','hotel_video']

        def get_average_rating(self, obj):
            return obj.get_average_rating()


class HotelDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

        def get_average_rating(self, obj):
            return obj.get_average_rating()


class HotelPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelPhotos
        fields = '__all__'


class RoomListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_price','all_inclusive']


class RoomDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoomPhotos
        fields = '__all__'


class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'