from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('car/<int:id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/add_review/', views.add_review, name='add_review'),
    path('about/', views.about, name='about'),
    path('book/<int:id>/', views.book_car, name='book_car'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('pay/<int:id>/', views.pay, name='pay'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_car/', views.add_car, name='add_car'),
    path('edit_car/<int:id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:id>/', views.delete_car, name='delete_car'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('view_cars/', views.view_cars, name='view_cars'),
    path('search/', views.search, name='search'),
    path('approve_booking/<int:id>/', views.approve_booking, name='approve_booking'),
    path('cancel_booking_admin/<int:id>/', views.cancel_booking_admin, name='cancel_booking_admin'),
    path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
]
