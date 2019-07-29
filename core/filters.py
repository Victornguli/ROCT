from django import forms
from .models import RO, CO, BU, Template
import django_filters

class TemplateFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr = "contains")
    regional_office = django_filters.ModelChoiceFilter(queryset=RO.objects.all(), widget=forms.Select)
    country_office = django_filters.ModelChoiceFilter(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = django_filters.ModelChoiceFilter(queryset=BU.objects.all(), widget=forms.Select)

    class Meta:
        model = Template
        fields = ["name",'regional_office', 'country_office', 'business_unit']
