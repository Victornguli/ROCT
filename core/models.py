from django.db import models
from django.contrib.auth.models import User


class RO(models.Model):
    ro_name = models.CharField(max_length=100, verbose_name="Regional office name")

    class Meta:
        verbose_name = "Regional Office"

    def __str__(self):
        return self.ro_name


class CO(models.Model):
    co_name = models.CharField(max_length=100, verbose_name="Country Office Name")

    class Meta:
        verbose_name = "Country Office"
        verbose_name_plural = "Country Offices"

    def __str__(self):
        return self.co_name


class BU(models.Model):
    bu_name = models.CharField(max_length=100, verbose_name="Unit name")

    class Meta:
        verbose_name = "Business Unit"

    def __str__(self):
        return self.bu_name


class Section(models.Model):
    section_name = models.CharField(max_length=100, verbose_name="Section name")
    # template = models.ManyToManyField("Template", verbose_name="template")
    # oversight = models.ManyToManyField("OversightReport", verbose_name="OVersight Report", null=True)

    class Meta:
        verbose_name = "Section"

    def __str__(self):
        return self.section_name


class TemplateSection(models.Model):
    section_name = models.CharField(max_length=100, verbose_name="Section name")


    class Meta:
        verbose_name = "Template Section"

    def __str__(self):
        return self.section_name    


class Area(models.Model):
    risk_choices = (
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    )
    area_name = models.CharField(max_length=100, verbose_name="Area name", null=True)
    expected_controls = models.CharField(max_length=1000, verbose_name="Expected Controls", null=True)
    findings = models.CharField(max_length=1000, verbose_name="Findings", null=True)
    risk = models.CharField(max_length=50, choices=risk_choices, verbose_name="Risk Severity", null=True)
    recommendation = models.CharField(max_length=1000, verbose_name="Recommendation", null=True)
    comment = models.CharField(max_length=1000, verbose_name="Management Comment", null=True)
    implementation_date = models.DateField(auto_now_add=False, verbose_name="Target Implementation Date", null=True)
    section = models.ForeignKey("Section", verbose_name="Section", on_delete=models.CASCADE, null=True)
    implementation_comment = models.CharField(max_length=1000, null=True, verbose_name = "Implementation Comment")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Area"

    def __str__(self):
        return self.area_name



class TemplateArea(models.Model):
    area_name = models.CharField(max_length=100, verbose_name="Area name", null=True)
    expected_controls = models.CharField(max_length=1000, verbose_name="Expected Controls", null=True)
    template_section = models.ForeignKey("TemplateSection", verbose_name="Template Section", on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Template Area"

    def __str__(self):
        return self.area_name    



class Template(models.Model):
    template_name = models.CharField(max_length=100, verbose_name="Template Title")
    regional_office = models.ForeignKey("RO", verbose_name="Regional Office", on_delete=models.CASCADE)
    country_office = models.ForeignKey("CO", verbose_name="Country Office", on_delete=models.CASCADE)
    business_unit = models.ForeignKey("BU", verbose_name="Business Unit", on_delete=models.CASCADE)
    template_areas = models.ManyToManyField("TemplateArea", verbose_name="Template Areas")
    template_sections = models.ManyToManyField("TemplateSection", verbose_name="Sections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    # oversight_report = models.ForeignKey("")

    class Meta:
        verbose_name = "Template"

    def __str__(self):
        return self.template_name


class Oversight(models.Model):
    oversight_status = (
        ("new", "New"),
        ("ongoing", "Ongoing"),
        ("follow_up", "Follow Up"),
        ("closed", "Closed"),
    )
    
    oversight_name = models.CharField(max_length=100, verbose_name="Oversight Name")
    template = models.ForeignKey("Template", verbose_name="Template", null=True, on_delete=models.CASCADE)
    # close_year = models.DateField(auto_now=False, auto_now_add=False, null=True, verbose_name="Year")
    status = models.CharField(max_length=50, choices=oversight_status, verbose_name="Status")

    regional_office = models.ForeignKey("RO", verbose_name="Regional Office", on_delete=models.CASCADE)
    country_office = models.ForeignKey("CO", verbose_name="Country Office", on_delete=models.CASCADE)
    business_unit = models.ForeignKey("BU", verbose_name="Business Unit", on_delete=models.CASCADE)
    areas = models.ManyToManyField("Area", verbose_name="Areas")
    sections = models.ManyToManyField("Section", verbose_name="Sections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    objectives = models.TextField(null=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)


    # Add User relationship
    class Meta:
        verbose_name = "Oversight"
        ordering = ["updated_at"]

    def __str__(self):
        return self.oversight_name
    

class TemplateCreator(models.Model):
    template_creators = models.ManyToManyField(User, verbose_name="Template Creators")


class MissionTeam(models.Model):
    mission = models.ForeignKey(Oversight, on_delete=models.CASCADE)
    mission_team = models.ManyToManyField(User, verbose_name = "Mission Team")


class FollowupTeam(models.Model):
    followup_team = models.ManyToManyField(User, verbose_name="Follow-up Team")


class Adminstrator(models.Model):
    adminstrators = models.ManyToManyField(User, verbose_name="Adminstrators")
