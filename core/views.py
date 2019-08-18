from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.encoding import smart_str
from django.forms import formset_factory
from django.db.models import Count, Max, Min

import csv
import datetime
import json

from .resources import OversightResource
from .models import Template, Area, Section, RO, CO, BU, Oversight
from .filters import TemplateFilter, OversightFilter
from .forms import AddAreaForm, AddSectionForm, AddTemplateForm, AddOversightForm, EditActiveAreaForm, EditFollowUpForm
# Create your views here.


# def export(request, oversight_id):
#     oversight_resource = OversightResource()
#     oversight  = Oversight.objects.filter(id=oversight_id)
#     dataset = oversight_resource.export(oversight)
#     response = HttpResponse(dataset.csv, content_type = "text/csv")
#     response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(oversight[0].oversight_name)
#     return response


def export(request, oversight_id):
    queryset = Oversight.objects.filter(pk=oversight_id)
    response = HttpResponse(content_type='text/csv')
    area_count = 0
    for obj in queryset:
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(obj.oversight_name)
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        # noinspection PyPackageRequirements
        writer.writerow([
            smart_str(u""),
            smart_str(u""),
            smart_str(u""),
            smart_str(u"{}".format(obj.oversight_name)),

            smart_str(u""),
            smart_str(u""),
            smart_str(u""),
            smart_str(u""),

        ])

    writer.writerow([
        smart_str(u"No"),
        smart_str(u"Area"),
        smart_str(u"Expected Controls"),
        smart_str(u"Findings"),
        smart_str(u"Risk Severity (High, Med, Low)"),
        smart_str(u"Recommendation"),
        smart_str(u"Management Comment"),
        smart_str(u"Target Implementation Date"),
    ])

    for obj in queryset:
        sections = Section.objects.filter(oversight__id = obj.id)
        for section in sections:
            writer.writerow([
                smart_str(u" "),
            ])
            writer.writerow([
                smart_str(u"{}".format(section.section_name)),
            ])
            areas = Area.objects.filter(section_id=section.id)         
            for area in areas:
                area_count += 1
                writer.writerow([
                    smart_str(u"{}".format(area_count)),
                    smart_str(u"{}".format(area.area_name)),
                    smart_str(u"{}".format(area.expected_controls)),
                    smart_str(u"{}".format(area.findings)),
                    smart_str(u"{}".format(area.risk)),
                    smart_str(u"{}".format(area.recommendation)),
                    smart_str(u"{}".format(area.comment)),
                    smart_str(u"{}".format(area.implementation_date)),
                ])
    return response


def filterTemplates(request):
    templates = Template.objects.all()
    template_filter = TemplateFilter(request.GET, queryset=templates)
    form = AddTemplateForm  

    context = {
        "templates":template_filter,
        "form":form,
    }
    return render(request, "core/templates.html", context)


def reports(request):
    ongoing = Oversight.objects.filter(status="ongoing").count()
    follow_up = Oversight.objects.filter(status="follow_up").count()
    closed = Oversight.objects.filter(status="closed").count()
    total = Oversight.objects.all().count()

    recently_updated = Oversight.objects.values("oversight_name", "status").annotate(
        recent = Max("areas__updated_at")).filter(
        areas__updated_at__gte=datetime.date.today() - datetime.timedelta(days=7)).order_by("-areas__updated_at")
    
    # recently_updated = Oversight.objects.filter(
    #     areas__updated_at__gte=datetime.date.today() - datetime.timedelta(days=7), 
    #     oversight_name__in=[item['oversight_name'] for item in distinct]
    #     ).order_by("-areas__updated_at")[:5]

    oversights = Oversight.objects.all()
    context = {
        "ongoing" : ongoing,
        "follow_up" : follow_up,
        "closed" : closed,
        "total" : total,
        "recently_updated" : recently_updated,
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
            template = Template.objects.create(
                template_name=template_name, regional_office=regional_office, 
                country_office=country_office, business_unit = business_unit)
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
    today = datetime.date.today()
    oversight = Oversight.objects.get(pk=oversight_id)
    # template = oversight.template
    sections = oversight.sections.all()
    areas = oversight.areas.all()
    #forms
    area_form = EditActiveAreaForm
    AreaFormSet = formset_factory(EditActiveAreaForm, extra=areas.count())
    formset = AreaFormSet()
    if request.method == "POST":
        formsets = AreaFormSet(request.POST)
        # area = Area.objects.get(pk=request.POST.copy()["area_id"])            
        # print(area_formsets)
        if formsets.is_valid():
            for formset in formsets:
                if formset.cleaned_data:
                    area_name = formset.cleaned_data.get("area_name")
                    expected_controls = formset.cleaned_data.get("expected_controls")
                    findings = formset.cleaned_data.get("findings")
                    risk = formset.cleaned_data.get("risk")
                    recommendation = formset.cleaned_data.get("recommendation")
                    comment = formset.cleaned_data.get("comment")
                    date = formset.cleaned_data.get("implementation_date")
                    area = Area.objects.get(pk=request.POST.copy()["area_id"])            
                    section = Section.objects.get(pk=request.POST.copy()["section_id"])
                    
                    # #Update Area
                    Area.objects.filter(pk=request.POST.copy()["area_id"]).update(
                        area_name=area_name, expected_controls=expected_controls,
                        findings=findings, risk=risk, recommendation=recommendation, 
                        comment=comment, implementation_date=date)

            # print(findings, risk, recommendation, comment, section, area)
            return redirect("edit_oversight", oversight_id=oversight_id)

    # for form in formset:
    #     print(form)

    context = {
        "oversight": oversight,
        "sections": sections,
        "areas": areas,
        "areas_and_areaforms": list(zip(
            areas,
            formset,
        )),
        "formset":formset,
        "area_form_media":area_form,
        "today": today,
    }

    return render(request, "core/edit_oversight.html", context)    


# Ajax call to this view to display relevant area form values for a specific area
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
    # print(data) Debug
    return JsonResponse(data)


def updateInline(request):
    if request.method == "GET":
        area_id = request.GET.get("area_id", None)
        area_name = request.GET.get("area_name", None)
        text = request.GET.get("text", None)

        if area_name == "area_name":
            area = Area.objects.filter(pk=area_id).update(area_name=text, updated_at=datetime.datetime.now())
        elif area_name == "expected_controls":
            area = Area.objects.filter(pk=area_id).update(expected_controls=text, updated_at=datetime.datetime.now())
        elif area_name == "findings":
            area = Area.objects.filter(pk=area_id).update(findings=text, updated_at=datetime.datetime.now())
        elif area_name == "risk":
            area = Area.objects.filter(pk=area_id).update(risk=text, updated_at=datetime.datetime.now())
            # pass
        elif area_name == "recommendation":
            area = Area.objects.filter(pk=area_id).update(recommendation=text, updated_at=datetime.datetime.now())
        elif area_name == "comment":
            area = Area.objects.filter(pk=area_id).update(comment=text, updated_at=datetime.datetime.now())
        elif area_name == "implementation_comment":
            area = Area.objects.filter(pk=area_id).update(implementation_comment=text, updated_at=datetime.datetime.now())            
        elif area_name == "implementation_date":
            # area = Area.objects.filter(pk=area_id).update(implementation_date=text)
            pass
        else:
            pass
        
        return HttpResponse("success")
        
        # print(area_id, area_name, text)
    return HttpResponse("error")   


def submitOversight(request, oversight_id):
    oversight = Oversight.objects.filter(pk=oversight_id).update(status = "follow_up")
    return redirect("follow_up")


def filterFollowUp(request):
    follow_up_missions = Oversight.objects.filter(status="follow_up")
    follow_up_filter = OversightFilter(queryset = follow_up_missions)
    context = {
        "oversights":follow_up_filter,
    }

    return render(request, "core/followup.html", context)


def editFollowUp(request, oversight_id):
    today = datetime.date.today()
    oversight = Oversight.objects.get(pk=oversight_id)
    # template = oversight.template
    sections = oversight.sections.all()
    areas = oversight.areas.all()
    #forms
    area_form = EditFollowUpForm
    
    if request.method == "POST":
        area_form = EditFollowUpForm(request.POST)
        if area_form.is_valid():
            implementation_comment = area_form.cleaned_data.get("implementation_comment")
            area = Area.objects.get(pk=request.POST.copy()["area_id"])            
            section = Section.objects.get(pk=request.POST.copy()["section_id"])
            
            #Update Area
            Area.objects.filter(pk=request.POST.copy()["area_id"]).update(implementation_comment=implementation_comment)

            return redirect("edit_follow_up", oversight_id=oversight_id)
            
    context = {
        "oversight": oversight,
        "sections": sections,
        "areas": areas,
        "area_form": area_form,
        "today": today,
    }

    return render(request, "core/edit_followup.html", context)    


def edit_oversight_ajax(request):
    if request.method == "POST":
        area_data = json.loads(request.POST.get("area_form_data"))
        return_fields = dict()

        for field in area_data:
            if "area_id" in field["name"]:
                area_id = field["value"]
                # print(area_id)

            elif "area_name" in field["name"]:
                area_name = field["value"]
                # print(area_name)  

            elif "expected_controls" in field["name"]:
                expected_controls = field["value"]
                # print(expected_controls)  

            elif "findings" in field["name"]:
                findings = field["value"]
                # print(findings)  

            elif "risk" in field["name"]:
                risk = field["value"]
                # print(risk)  

            elif "recommendation" in field["name"]:
                recommendation = field["value"]
                # print(recommendation)  

            elif "comment" in field["name"]:
                comment = field["value"]
                # print(comment)  

            elif "implementation_date" in field["name"]:
                imp_date = datetime.datetime.strptime(field["value"], '%Y-%m-%d').date()
                # print(type(imp_date))

            elif "area" in field["name"]:
                area = field["value"]
                # print(area)   

            elif "section" in field["name"]:
                section = field["value"]
                # print(section)                                                         

            else:
                pass

        if area_id is not None:
            Area.objects.filter(pk=area_id).update(
                area_name=area_name, expected_controls=expected_controls,
                findings=findings, risk=risk, recommendation=recommendation, 
                comment=comment, implementation_date = imp_date, updated_at=datetime.datetime.now())
            return_fields.update({"area_name":area_name, "findings":findings, "expected_controls":expected_controls, "risk":risk,
            "recommendation":recommendation, "comment":comment, "implementation_date":imp_date})                 

        return JsonResponse(return_fields)
    else:
        return HttpResponse("success")





def close_oversight(request, oversight_id):
    oversight = Oversight.objects.filter(pk=oversight_id).update(status="closed")
    return redirect ("follow_up")


def closed_oversights(request):
    closed_oversights = Oversight.objects.filter(status="closed")
    oversights = OversightFilter(queryset=closed_oversights)
    context = {
        "oversights":oversights,
    }

    return render(request, "core/closed.html", context)


def view_closed_oversight(request, oversight_id):
    oversight = Oversight.objects.get(pk=oversight_id)
    sections = Section.objects.filter(oversight__id = oversight_id)
    areas = Area.objects.filter(oversight__id=oversight_id)
    context = {
        "oversight":oversight,
        "sections":sections,
        "areas":areas,
    }

    return render(request, "core/view_closed.html", context)

