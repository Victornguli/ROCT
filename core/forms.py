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