from django.shortcuts import render, redirect

from .models import Template, Area, Section, RO, CO, BU
from .filters import TemplateFilter
from .forms import AddAreaForm, AddSectionForm, AddTemplateForm
# Create your views here.

def filterTemplates(request):
    templates = Template.objects.all()
    template_filter = TemplateFilter(request.GET, queryset=templates)
    form = AddTemplateForm

    context = {
        "templates":template_filter,
        "form":form,
    }
    return render(request, "core/index.html", context)


def loadTemplate(request, template_id):
    template = Template.objects.get(pk=template_id)
    sections = Section.objects.filter(template__id=template_id)
    areas = Area.objects.filter(template__id=template_id)
    form = AddTemplateForm()
    context = {
        "template":template,
        "sections":sections,
        "areas":areas,
        "form":form,
    }

    return render(request, "core/load.html", context)


def defineTemplate(request):
    form = AddTemplateForm
    if request.method == "POST":
        form = AddTemplateForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            regional_office = RO.objects.get(ro_name = form.cleaned_data.get("regional_office"))
            country_office = CO.objects.get(co_name = form.cleaned_data.get("country_office"))
            business_unit = BU.objects.get(bu_name = form.cleaned_data.get("business_unit"))
            template_name = form.cleaned_data.get("template_name")
            
            #Create new Template
            template = Template.objects.create(template_name=template_name, regional_office =regional_office, country_office=country_office, business_unit = business_unit)
            # print (regional_office, country_office, business_unit, template_name)
            return redirect("edit_template", template_id = template.id)

        else:
            return redirect("filter_templates")
    return redirect("filter_templates")


def editTemplate(request, template_id):
    section_form = AddSectionForm
    area_form = AddAreaForm
    template = Template.objects.get(pk=template_id)
    sections = Section.objects.filter(template__id = template_id)
    areas = Area.objects.all()
    context = {
        "section_form":section_form,
        "area_form":area_form,
        "template":template,
        "sections":sections,
        "areas":areas,
    }

    if request.method == "POST":
        section_form = AddSectionForm(request.POST)
        area_form = AddAreaForm(request.POST)

        #Handle Add Sections
        if section_form.is_valid():
            print("Request _section")
            section_name = section_form.cleaned_data.get("section_name")
            section = Section.objects.create(section_name = section_name)
            section.template.add(template) #many to many rel-ship

            return redirect("edit_template", template_id=template.id)
        else:
            section_form = AddSectionForm

        # Handle Add Areas...
        if area_form.is_valid():
            area_name = area_form.cleaned_data.get("area_name")
            expected_controls = area_form.cleaned_data.get("expected_controls")
            print(request.POST.copy()["section_id"])
            section = Section.objects.get(pk=request.POST.copy()["section_id"])
            area = Area.objects.create(area_name = area_name, expected_controls = expected_controls, section=section)
            print(area)

            return redirect("edit_template", template_id=template.id)


    else:
        return render(request, "core/edit_template.html", context)
