from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='car_images')
    is_available = models.BooleanField(default=True)
    city = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name
    
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + ' - ' + self.car.name

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
    ]

    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS)
    card_number = models.CharField(max_length=16, validators=[RegexValidator(regex=r'^\d{16}$', message='Card number must be 16 digits.')])
    card_holder = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=5, validators=[RegexValidator(regex=r'^\d{2}/\d{2}$', message='Expiry date must be in MM/YY format.')])
    cvv = models.CharField(max_length=3, validators=[RegexValidator(regex=r'^\d{3}$', message='CVV must be 3 digits.')])
    amount = models.IntegerField()

    def __str__(self):
        return self.booking.user.username + ' - ' + self.booking.car.name  
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.car.name}'
