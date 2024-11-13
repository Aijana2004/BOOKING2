
from rest_framework import viewsets, status, generics,permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .filters import HotelFilter,RoomFilter
from .permissions import CheckOwner,CheckCRUD,CheckOwnerHotel,CheckRoom,CheckBooking,\
    CheckReview,CheckRoomOwner,CheckBookUser,CheckPhotos


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers


class HotelListViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields= ['country','city','hotel_stars']
    search_fields = ['hotel_name']
    ordering_fields = ['hotel_stars']
    permission_classes = [CheckCRUD,CheckOwnerHotel]


class HotelDetailViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializers
    permission_classes = [CheckCRUD,CheckOwnerHotel]


class HotelPhotosViewSet(viewsets.ModelViewSet):
    queryset = HotelPhotos.objects.all()
    serializer_class = HotelPhotosSerializers
    permission_classes = [CheckPhotos]


class RoomListViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializers
    filterset_class = RoomFilter
    permission_classes = [CheckRoomOwner]


class RoomDetailViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializers
    filterset_class = RoomFilter
    permission_classes = [CheckRoom,CheckRoomOwner]


class RoomPhotosViewSet(viewsets.ModelViewSet):
    queryset = RoomPhotos.objects.all()
    serializer_class = RoomPhotosSerializers
    permission_classes = [CheckPhotos]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializers
    permission_classes = [CheckBooking,CheckBookUser]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         booking = serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [permissions.IsAuthenticated,CheckOwner,CheckReview]



