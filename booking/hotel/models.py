from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('SimpleUser', 'SimpleUser'),
        ('OwnerUser', 'OwnerUser')
    )
    user_role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='SimpleUser')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(80)], null=True, blank=True)


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=32)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_description = models.TextField()
    country = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    TYPE_CHOICES =()
    hotel_stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                               MaxValueValidator(5)])
    hotel_video = models.FileField(upload_to='hotel_video/', null=True, blank=True)
    created_date = models.DateField(auto_now=True)

    def str(self):
        return f'{self.hotel_name}, {self.country}, {self.city}'

    def get_average_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class HotelPhotos(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_image = models.ImageField(upload_to='hotel_images/')


class Room(models.Model):
    room_number = models.PositiveSmallIntegerField()
    hotel_room = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    TYPE_CHOICES = (
        ('VIP','VIP'),
        ('стандартный','стандартный'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный'),
    )
    room_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят'),
    )
    room_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='свободен')
    room_price = models.PositiveIntegerField()
    all_inclusive = models.BooleanField(default=False)
    room_description = models.TextField()

    def str(self):
        return f'{self.hotel_room} - {self.room_number} - {self.room_type}'


class RoomPhotos(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    room_image = models.ImageField(upload_to='room_images/')


class Review(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)], null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def str(self):
        return f'{self.user_name}, {self.hotel} - {self.stars}'


class Booking(models.Model):
    hotel_book = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_book = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_book = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_price = models.PositiveIntegerField(default=0)
    STATUS_BOOK_CHOICES = (
        ('отменено', 'отменено'),
        ('подтверждено', 'подтверждено'),
    )
    status_book = models.CharField(max_length=16, choices=STATUS_BOOK_CHOICES)

    def str(self):
        return f'{self.user_book}, {self.hotel_book}, {self.status_book}'

    class Meta:
        unique_together = ('room_book', 'check_in', 'check_out')


    def clean(self):
        # Проверка на доступность комнаты
        if not self.is_room_available():
            raise ValidationError("Эта комната уже забронирована на указанные даты.")

        # Проверка на корректность дат
        if self.check_in >= self.check_out:
            raise ValidationError("Дата выезда должна быть позже даты заезда.")

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        self.room_book.room_status = 'забронирован'
        self.room_book.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.room_book.room_status = 'свободен'
        self.room_book.save()
        super().delete(*args, **kwargs)

    def calculate_total_price(self):
        num_days = (self.check_out - self.check_in).days
        self.total_price = num_days * self.room_book.room_price

    def is_room_available(self):
        overlapping_bookings = Booking.objects.filter(
            room_book=self.room_book,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(pk=self.pk)
        return not overlapping_bookings.exists()