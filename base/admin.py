from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Car, Booking

def admin_dashboard(request):
    cars = Car.objects.all()
    bookings = Booking.objects.all()
    users = User.objects.all()  # Fetch all users including their emails
    return render(request, 'base/admin_dashboard.html', {'cars': cars, 'bookings': bookings, 'users': users})
