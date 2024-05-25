from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking, User, Payment , Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from .forms import PaymentForm, CarForm, ReviewForm , UserEditForm, SignUpForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
import re
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Home page view
def home(request):
    cars = Car.objects.all()[:6]
    return render(request, 'base/home.html', {'cars': cars})

# Car detail view
def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    reviews = Review.objects.filter(car=car)
    return render(request, 'base/car_detail.html', {'car': car, 'reviews': reviews})

# About page view
def about(request):
    return render(request, 'base/about.html')

# Booking a car view
@login_required
def book_car(request, id):
    car = get_object_or_404(Car, id=id)
    error_message = None

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        today = timezone.now().date()

        if start_date < str(today):
            error_message = 'Start date cannot be in the past.'
        elif end_date < start_date:
            error_message = 'End date cannot be before start date.'
        elif Booking.objects.filter(car=car, start_date__lte=end_date, end_date__gte=start_date).exists():
            error_message = 'The car is already booked for the selected dates.'
        
        if error_message:
            return render(request, 'base/book_car.html', {'car': car, 'error_message': error_message})
        
        booking = Booking(user=request.user, car=car, start_date=start_date, end_date=end_date)
        booking.save()
        return redirect(reverse('home'))
    
    return render(request, 'base/book_car.html', {'car': car})

# Viewing user's bookings
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'base/my_bookings.html', {'bookings': bookings})

# User signup view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'base/signup.html', {'form': form})

# User signin view
def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        
        # Check if the input is an email address
        if '@' in username_or_email:
            kwargs = {'email': username_or_email}
        else:
            kwargs = {'username': username_or_email}
        
        # Authenticate user using either username or email
        user = authenticate(request, **kwargs, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
    
    return render(request, 'base/signin.html')

# User signout view
@login_required
def signout(request):
    logout(request)
    return redirect(reverse('home'))

# Cancel booking view
@login_required
def cancel_booking(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Your booking has been successfully cancelled.')
        return redirect(reverse('my_bookings'))
    
    return render(request, 'base/cancel_booking.html', {'booking': booking})

# Payment view
@login_required
def pay(request, id):
    booking = get_object_or_404(Booking, id=id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number'].replace(' ', '')
            expiry_date = form.cleaned_data['expiry_date']
            month, year = expiry_date.split('/')
            month = int(month)
            year = int(year) + 2000
            current_year = datetime.now().year
            current_month = datetime.now().month
            if year < current_year or (year == current_year and month < current_month):
                form.add_error('expiry_date', 'Expiry date is in the past.')
            if not form.errors:
                payment = form.save(commit=False)
                payment.booking = booking
                payment.amount = booking.car.price
                payment.save()
                booking.is_approved = True
                booking.save()
                return redirect(reverse('my_bookings'))
    else:
        form = PaymentForm()
    return render(request, 'base/pay.html', {'form': form, 'booking': booking})



# Admin: Add a car view
@staff_member_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CarForm()
    return render(request, 'base/add_car.html', {'form': form})

# Admin: Edit a car view
@staff_member_required
def edit_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CarForm(instance=car)
    return render(request, 'base/edit_car.html', {'form': form, 'car': car})

# Admin: Delete a car view
@staff_member_required
def delete_car(request, id):
    car = get_object_or_404(Car, id=id)
    car.image.delete()
    car.delete()
    return redirect('admin_dashboard')

# Admin: Approve a booking view
@staff_member_required
def approve_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.is_approved = True
    booking.save()
    return redirect('admin_dashboard')

# Admin: Cancel a booking view
@staff_member_required
def cancel_booking_admin(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return redirect('admin_dashboard')

# Admin: Edit a user view
@staff_member_required
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('admin_dashboard')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'base/edit_user.html', {'form': form})

# Admin: Delete a user view
@staff_member_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('admin_dashboard')

# Admin: View all bookings
@staff_member_required
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'base/view_bookings.html', {'bookings': bookings})

# Admin dashboard view
@staff_member_required
def admin_dashboard(request):
    cars = Car.objects.all()
    bookings = Booking.objects.all()
    users = User.objects.all()
    return render(request, 'base/admin_dashboard.html', {'cars': cars, 'bookings': bookings, 'users': users})

# View all cars
def view_cars(request):
    car_list = Car.objects.all().order_by('id')  # Ensure consistent ordering
    paginator = Paginator(car_list, 6)  # Show 6 cars per page
    page = request.GET.get('page')

    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)

    return render(request, 'base/view_cars.html', {'cars': cars})

# Search view
def search(request):
    query = request.GET.get('q', '')
    results = Car.objects.none()
    
    if query:
        results = Car.objects.filter(
            Q(name__icontains=query) |
            Q(model__icontains=query) |
            Q(year__icontains=query) |
            Q(price__icontains=query)
        )
        
    paginator = Paginator(results, 6)  # Show 6 results per page.
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'base/search.html', {'results': results, 'query': query})


@login_required
def add_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.car = car
            review.save()
            return redirect('car_detail', id=car.id)
    else:
        form = ReviewForm()
    return render(request, 'base/add_review.html', {'form': form, 'car': car})
