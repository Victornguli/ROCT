from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse



from .models import Template, Area, Section, RO, CO, BU, Oversight
from .filters import TemplateFilter, OversightFilter
from .forms import AddAreaForm, AddSectionForm, AddTemplateForm, AddOversightForm, EditActiveAreaForm
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
    oversight = Oversight.objects.create(oversight_name="{} Oversight".format(template.template_name), template=template, regional_office=ro, country_office=co, business_unit=bu, status="ongoing")
    for section in sections:
        oversight.sections.add(section)
    
    for area in areas:
        oversight.areas.add(area)

    return redirect("edit_oversight", oversight_id=oversight.id)


def ongoingOversight(request):
    oversights = Oversight.objects.all()
    oversight_filter = OversightFilter(request.GET, queryset=oversights)
    context = {
        "oversights": oversight_filter,
    }

    return render(request, "core/ongoing.html", context)


def editOversight(request, oversight_id):
    oversight = Oversight.objects.get(pk=oversight_id)
    # template = oversight.template
    sections = oversight.sections.all()
    areas = oversight.areas.all()
    #forms
    area_form = EditActiveAreaForm
    
    if request.method == "POST":
        area_form = EditActiveAreaForm(request.POST)
        if area_form.is_valid():
            findings = area_form.cleaned_data.get("findings")
            risk = area_form.cleaned_data.get("risk")
            recommendation = area_form.cleaned_data.get("recommendation")
            comment = area_form.cleaned_data.get("comment")
            date = area_form.cleaned_data.get("implementation_date")
            area = Area.objects.get(pk=request.POST.copy()["area_id"])            
            section = Section.objects.get(pk=request.POST.copy()["section_id"])
            
            #Update Area
            Area.objects.filter(pk=request.POST.copy()["area_id"]).update(findings=findings, risk=risk, recommendation=recommendation, comment=comment, implementation_date=date)

            print(findings, risk, recommendation, comment, section, area)
            return redirect("edit_oversight", oversight_id=oversight_id)
            
    context = {
        "oversight": oversight,
        "sections": sections,
        "areas": areas,
        "area_form": area_form,
    }

    return render(request, "core/edit_oversight.html", context)    


#Ajax call to this view to display relevant area form values for a specific area
def renderAreaForm(request):
    area_id = request.GET.get("area_id",None)
    area = Area.objects.get(pk=area_id)
    data = {
        "area_name":area.area_name,
        "expected_controls":area.expected_controls,
        "findings":area.findings,
        "risk":area.risk,
        "recommendation":area.recommendation,
        "comment":area.comment,
        "implementation_date":area.implementation_date,
    }
    print(data)
    return JsonResponse(data)