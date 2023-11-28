from django.db.models import Q
import django_filters

from epic_crm.models import Client, Contract, Event


# TODO anadir un filtro para filtrar usarios por equipos

class ClientFilter(django_filters.FilterSet):

    full_name = django_filters.CharFilter(method='filter_name')
    email = django_filters.CharFilter(field_name="email", lookup_expr='icontains')
    sales_contact = django_filters.CharFilter(field_name="sales_contact")

    class Meta:
        model = Client
        fields = []

    def filter_name(self, queryset, name, value):
        queryset = queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))

        return queryset


class ContractFilter(django_filters.FilterSet):

    client_name = django_filters.CharFilter(method='filter_client_name')
    client_email = django_filters.CharFilter(field_name="client__email", lookup_expr='icontains')
    updated_after = django_filters.DateTimeFilter(field_name="date_updated", lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name="date_updated", lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')
    is_signed = django_filters.BooleanFilter(field_name="is_signed")

    class Meta:
        model = Contract
        fields = []

    def filter_client_name(self, queryset, name, value):
        queryset = queryset.filter(Q(client__first_name__icontains=value) | Q(client__last_name__icontains=value))
        return queryset


class EventFilter(django_filters.FilterSet):

    client_name = django_filters.CharFilter(method='filter_client_name')
    client_email = django_filters.CharFilter(field_name="client__email", lookup_expr='icontains')
    event_after = django_filters.DateTimeFilter(field_name="event_date", lookup_expr='gte')
    event_before = django_filters.DateTimeFilter(field_name="event_date", lookup_expr='lte')
    # TODO anadir un filtro pa el estado


    class Meta:
        model = Event
        fields = []

    # TODO factorize this functio to avoid repetition with ContractFilter
    def filter_client_name(self, queryset, name, value):
        queryset = queryset.filter(Q(client__first_name__icontains=value) | Q(client__last_name__icontains=value))
        return queryset