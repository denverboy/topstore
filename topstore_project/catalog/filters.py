from django_filters import rest_framework as r_f


class CatalogFilter(r_f.FilterSet):
    name = r_f.CharFilter(field_name='title', lookup_expr='icontains')
    minPrice = r_f.NumberFilter(field_name='price', lookup_expr='gte')
    maxPrice = r_f.NumberFilter(field_name='price', lookup_expr='lte')
    available = r_f.BooleanFilter(method='get_availability')
    free_delivery = r_f.BooleanFilter()

    def get_availability(self, queryset, name, value):
        if value:
            return queryset.exclude(count=0)
        return queryset
