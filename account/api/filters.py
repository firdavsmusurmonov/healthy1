# import django_filters
# from account.models import Customuser
# class ProductFilter(django_filters.FilterSet):
#     flash_sale = django_filters.BooleanFilter(field_name='flash_sale')
#     name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
#     # price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
#     # price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

#     class Meta:
#         model = Customuser
#         fields = ["flash_sale", 'mega_sale', 'home_sale', 'name']


# # class NotificationFilter(django_filters.FilterSet):
# #     notifation_type = django_filters.ModelChoiceFilter(queryset=NotifationType.objects.all())

# #     class Meta:
# #         model = Notifation
# #         fields = ["notifation_type"]