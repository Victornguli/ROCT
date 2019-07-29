from django.shortcuts import render

from .models import Template, Area, Section
from .filters import TemplateFilter
from .forms import AddAreaForm
# Create your views here.

def filterTemplates(request):
    templates = Template.objects.all()
    template_filter = TemplateFilter(request.GET, queryset=templates)
    context = {
        "templates":template_filter,
    }
    return render(request, "core/index.html", context)


def loadTemplate(request, template_id):
    template = Template.objects.get(pk=template_id)
    sections = Section.objects.filter(template__id=template_id)
    areas = Area.objects.filter(template__id=template_id)
    form = AddAreaForm
    context = {
        "template":template,
        "sections":sections,
        "areas":areas,
        "form":form,
    }


    for area in areas:
        print (area)

    return render(request, "core/load.html", context)
    