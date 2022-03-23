import django_filters
from account.models import Diagnos, Disease, Customuser


class CustomuserFilter(django_filters.FilterSet):
    is_doctor = django_filters.BooleanFilter(field_name='is_doctor')
    fullname = django_filters.CharFilter(field_name='fullname', lookup_expr='icontains')

    class Meta:
        model = Customuser
        fields = ["is_doctor", 'profession', 'city', 'region']


class DiagnosFilter(django_filters.FilterSet):
    disease = django_filters.ModelChoiceFilter(queryset=Disease.objects.all())

    class Meta:
        model = Diagnos
        fields = ["disease"]
