from django import forms
from .models import RO, CO, BU, Template, Oversight
import django_filters

class TemplateFilter(django_filters.FilterSet):
    template_name = django_filters.CharFilter()
    regional_office = django_filters.ModelChoiceFilter(queryset=RO.objects.all(), widget=forms.Select)
    country_office = django_filters.ModelChoiceFilter(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = django_filters.ModelChoiceFilter(queryset=BU.objects.all(), widget=forms.Select)

    class Meta:
        model = Template
        fields = ["template_name",'regional_office', 'country_office', 'business_unit']



class OversightFilter(django_filters.FilterSet):
    close_year = django_filters.NumberFilter(field_name='start_date', lookup_expr='year')
    regional_office = django_filters.ModelChoiceFilter(queryset=RO.objects.all(), widget=forms.Select)
    country_office = django_filters.ModelChoiceFilter(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = django_filters.ModelChoiceFilter(queryset=BU.objects.all(), widget=forms.Select)

    class Meta:
        model = Oversight
        fields = ["close_year", "regional_office", "country_office", "business_unit"]


class FollowupFilter(django_filters.FilterSet):
    close_year = django_filters.CharFilter()
    regional_office = django_filters.ModelChoiceFilter(queryset=RO.objects.all(), widget=forms.Select)
    country_office = django_filters.ModelChoiceFilter(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = django_filters.ModelChoiceFilter(queryset=BU.objects.all(), widget=forms.Select)

    class Meta:
        model = Oversight
        fields = ["close_year", "regional_office", "country_office", "business_unit"]


class ReportsFilter(django_filters.FilterSet):
    close_year = django_filters.NumberFilter(field_name='start_date', lookup_expr='year')
    regional_office = django_filters.ModelChoiceFilter(queryset=RO.objects.all(), widget=forms.Select)
    country_office = django_filters.ModelChoiceFilter(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = django_filters.ModelChoiceFilter(queryset=BU.objects.all(), widget=forms.Select)

    class Meta:
        model = Oversight
        fields = ["regional_office", "country_office", "business_unit"]

