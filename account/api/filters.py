# import django_filters
# from account.models import Customuser
# class DoctorFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
#     class Meta:
#         model = Customuser
#         fields = ["flash_sale", 'mega_sale', 'home_sale', 'name']

#
# class NotificationFilter(django_filters.FilterSet):
#     notifation_type = django_filters.ModelChoiceFilter(queryset=NotifationType.objects.all())
#
#     class Meta:
#         model = Notifation
#         fields = ["notifation_type"]