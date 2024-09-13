# filters.py

import django_filters
from next_of_kin.models import NextOfKin

class NextOfKinFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    id = django_filters.NumberFilter()

    class Meta:
        model = NextOfKin
        fields = ['first_name', 'id']
