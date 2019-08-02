from django.shortcuts import render, redirect

from .models import Template, Area, Section, RO, CO, BU, Oversight
from .filters import TemplateFilter
from .forms import AddAreaForm, AddSectionForm, AddTemplateForm, AddOversightForm, addActiveAreasForm
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
    section_form = AddSectionForm()
    area_form = AddAreaForm()
    # section_form = AddSectionForm()
    context = {
        "template":template,
        "sections":sections,
        "areas":areas,
        "section_form":section_form,
        "area_form":area_form,
    }
    print(context["template"])

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
    oversight_form = AddOversightForm
    template = Template.objects.get(pk=template_id)
    sections = template.sections.all()
    areas = template.areas.all()
    context = {
        "section_form": section_form,
        "area_form": area_form,
        "oversight_form": oversight_form,
        "template": template,
        "sections": sections,
        "areas": areas,
    }

    if request.method == "POST":
        section_form = AddSectionForm(request.POST)
        area_form = AddAreaForm(request.POST)

        #Handle Add Sections
        if section_form.is_valid():
            print("Request _section")
            section_name = section_form.cleaned_data.get("section_name")
            section = Section.objects.create(section_name = section_name)
            template.sections.add(section) #many to many rel-ship

            return redirect("edit_template", template_id = template.id)
        else:
            section_form = AddSectionForm

        # Handle Add Areas...
        if area_form.is_valid():
            area_name = area_form.cleaned_data.get("area_name")
            expected_controls = area_form.cleaned_data.get("expected_controls")
            print(request.POST.copy()["section_id"])
            section = Section.objects.get(pk=request.POST.copy()["section_id"])
            area = Area.objects.create(area_name = area_name, expected_controls = expected_controls, section=section)
            template.areas.add(area)

            return redirect("edit_template", template_id=template.id)

    else:
        return render(request, "core/edit_template.html", context)


def startOversight(request, template_id):
    template = Template.objects.get(pk=template_id)
    # save_template = request.GET.copy()["save_template"]
    # print(save_template)
    # if save_template == "yes":
    #     #Save this template( Already done.. so keep it)
    #     pass
    # else:
    #     #delete this template
    #     pass

    ro = template.regional_office
    co = template.country_office
    bu = template.business_unit
    sections = template.sections.all()
    areas = template.areas.all()
    oversight = Oversight.objects.create(oversight_name="{} ".format(template.template_name), template=template, regional_office=ro, country_office=co, business_unit=bu, status="ongoing")
    for section in sections:
        oversight.sections.add(section)
    
    for area in areas:
        oversight.areas.add(area)

    return redirect("ongoing_oversight", oversight_id=oversight.id)


def ongoingOversight(request, oversight_id):
    oversight = Oversight.objects.get(pk=oversight_id)
    template = oversight.template
    sections = template.sections.all()
    areas = template.areas.all()

    #forms
    area_form = AddAreaForm
    
    context = {
        "oversight": oversight,
        "sections": sections,
        "areas": areas,
        "area_form": area_form,
    }

    return render(request, "core/ongoing.html", context)