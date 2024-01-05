import django_filters


class RoomFilter(django_filters.FilterSet):
    size = django_filters.NumberFilter(lookup_expr='exact')
    size__gt = django_filters.NumberFilter(
        field_name='size',
        lookup_expr='gt'
    )
    size__lt = django_filters.NumberFilter(
        field_name='size',
        lookup_expr='lt'
    )
    accommodation = django_filters.NumberFilter(lookup_expr='exact')
    description = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter(lookup_expr='exact')
    price__gt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gt'
    )
    price__lt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lt'
    )

    # Filter by foreign key
    floor = django_filters.NumberFilter(
        field_name='floor__level',
        lookup_expr='eq'
    )


class MenuItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter(lookup_expr='exact')
    price__gt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gt'
    )
    price__lt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lt'
    )

    description = django_filters.CharFilter(lookup_expr='icontains')

    # Filter by foreign key
    restaurant = django_filters.NumberFilter(
        field_name='restaurants__id',
        lookup_expr='eq'
    )

    q = django_filters.CharFilter(method='filter_by_q', label='Search')

    def filter_by_q(self, queryset, name, value):
        return queryset.filter(name__icontains=value) \
            | queryset.filter(description__icontains=value)
