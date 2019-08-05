from django import forms
from django.forms import ModelForm
from .models import RO,CO,BU,Template,Area


class DateInput(forms.DateInput):
    input_type = 'date'



class AddAreaForm(forms.Form):
    area_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Area Name'}), help_text="Type in the name of the area")
    expected_controls = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={'placeholder':'Expected Controls',"rows":"3", "cols":"2"}))
    # findings = forms.CharField(max_length=100, required=False, widget=forms.Textarea(attrs={'placeholder':'Findings'}), help_text="Type in the name of the area")
    # risk = forms.ModelChoiceField(required=False, widget=forms.Select(), help_text="Type in the name of the area")

    # class Meta:
    #     model = Area
    #     fields = ["risk"]

class EditActiveAreaForm(forms.Form):
    risk_choices = (
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    )
    
    area_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Area Name'}), help_text="Type in the name of the area")
    expected_controls = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={'placeholder':'Expected Controls',"rows":"4", "cols":"2"}))

    findings = forms.CharField(max_length=1000, required=False, widget=forms.Textarea(attrs={'placeholder':'Findings', "rows":"4", "cols":"2"}), help_text="Type in the name of the area")
    risk = forms.ChoiceField(choices=risk_choices, required=False, widget=forms.Select(), help_text="Select Risk")
    recommendation = forms.CharField(max_length=1000, required=False, widget=forms.Textarea(attrs={'placeholder':'Recommendations', "rows":"4", "cols":"2"}), help_text="Enter any recommendations")
    comment = forms.CharField(max_length=1000, required=False, widget=forms.Textarea(attrs={'placeholder':'Management Comments', "rows":"4", "cols":"2"}), help_text="Enter Management Comment")
    implementation_date = forms.DateField(required=False, widget=DateInput())

    class Meta:
        model = Area
        fields = ["risk"]


class AddSectionForm(forms.Form):
    section_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Section Name'}), help_text="Type in the name of the section")


class AddTemplateForm(forms.Form):
    regional_office = forms.ModelChoiceField(queryset=RO.objects.all(), widget=forms.Select)
    country_office = forms.ModelChoiceField(queryset=CO.objects.all(), widget=forms.Select)
    business_unit = forms.ModelChoiceField(queryset=BU.objects.all(), widget=forms.Select)
    template_name = forms.CharField(max_length=200, required=True)

class AddOversightForm(forms.Form):
    oversight_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'Oversight Name'}), help_text="Type in the name of this Oversight Mission")
    close_year = forms.DateField(widget=forms.SelectDateWidget())
