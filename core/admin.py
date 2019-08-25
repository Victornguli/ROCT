from django.contrib import admin
from .models import RO, CO, BU, Section, TemplateSection, Area, TemplateArea, Template, Oversight
from django.http import HttpResponse
# Register your models here.

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    area_count = 0
    for obj in queryset:
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(obj.oversight_name)
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"{}".format(obj.oversight_name)),
        ])

    writer.writerow([
        smart_str(u"NO"),
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
    
export_csv.short_description = u"Export CSV"

class OversightAdmin(admin.ModelAdmin):
    actions = [export_csv]
    list_display = ("oversight_name", "created_at", "updated_at")

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("area_name", "updated_at")


@admin.register(TemplateArea)
class TemplateAreaAdmin(admin.ModelAdmin):
    list_display = ("area_name", "updated_at")


@admin.register(TemplateSection)
class TemplateSectionAdmin(admin.ModelAdmin):
    list_display = ("section_name",)



admin.site.register(RO)
admin.site.register(CO)
admin.site.register(BU)
admin.site.register(Section)
admin.site.register(Template)
admin.site.register(Oversight, OversightAdmin)
