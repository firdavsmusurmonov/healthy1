import django_filters
from account.models import Diagnos, Disease
# class DoctorFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
#     class Meta:
#         model = Customuser
#         fields = ["flash_sale", 'mega_sale', 'home_sale', 'name']

#
class DiagnosFilter(django_filters.FilterSet):
    disease = django_filters.ModelChoiceFilter(queryset=Disease.objects.all())

    class Meta:
        model = Diagnos
        fields = ["disease"]