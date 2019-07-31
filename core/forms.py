from django import forms
from django.forms import ModelForm
from .models import RO,CO,BU,Template,Area

class AddAreaForm(forms.Form):
    area_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Area Name'}), help_text="Type in the name of the area")
    expected_controls = forms.CharField(max_length=100, required=True, widget=forms.Textarea(attrs={'placeholder':'Expected Controls',"rows":"2", "cols":"2"}))
    # findings = forms.CharField(max_length=100, required=False, widget=forms.Textarea(attrs={'placeholder':'Findings'}), help_text="Type in the name of the area")
    # risk = forms.ModelChoiceField(required=False, widget=forms.Select(), help_text="Type in the name of the area")

    # class Meta:
    #     model = Area
    #     fields = ["risk"]


class AddSectionForm(forms.Form):
    section_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Section Name'}), help_text="Type in the name of the section")


class AddTemplateForm(forms.Form):
    regional_office = forms.ModelChoiceField(queryset=RO.objects.all(), widget=forms.Select)
    country_office = forms.ModelChoiceField(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = forms.ModelChoiceField(queryset=BU.objects.all(), widget=forms.Select)
    template_name = forms.CharField(max_length=200, required=True)

class AddOversightReportForm(forms.Form):
    oversight_report_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'Oversight Report Name'}), help_text="Type in the name of this Oversight Report")
    regional_office = forms.ModelChoiceField(queryset=RO.objects.all(), widget=forms.Select)
    country_office = forms.ModelChoiceField(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = forms.ModelChoiceField(queryset=BU.objects.all(), widget=forms.Select)