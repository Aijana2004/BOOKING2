from django_filters import FilterSet
from .models import Hotel,Room


class HotelFilter(FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'address': ['exact'],
            'hotel_name': ['exact'],


         }


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'room_price': ['gt', 'lt'],
            'room_number': ['exact'],

        }