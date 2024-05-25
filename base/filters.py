# filters.py
import django_filters
from .models import Car

class CarFilter(django_filters.FilterSet):
    # Define filters based on your model fields
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Car
        fields = ['make', 'model', 'year']  # Add more fields as needed
