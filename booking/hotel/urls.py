from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'hotel', HotelListViewSet, basename='hotel-list')
router.register(r'users', UserProfileViewSet,basename='users')
router.register(r'hotel-detail', HotelDetailViewSet,basename='hotel-detail')
router.register(r'room', RoomListViewSet,basename='room-list')
router.register(r'room-detail', RoomDetailViewSet,basename='room-detail')
router.register(r'review', ReviewViewSet,basename='review')
router.register(r'booking', BookingViewSet,basename='booking')


urlpatterns = [
    path('', include(router.urls)),


]