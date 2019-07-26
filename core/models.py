from django.db import models

# Create your models here.
class RO(models.Model):
    name = models.CharField(max_length=100, verbose_name="Regional office name")

    class Meta:
        verbose_name = "Regional Office"


class CO(models.Model):
    name = models.CharField(max_length=100, verbose_name="Country Office Name")

    class Meta:
        verbose_name = "Country Office"
        verbose_name_plural = "Country Offices"


class BU(models.Model):
    name = models.CharField(max_length=100, verbose_name="Unit name")

    class Meta:
        verbose_name = "Business Unit"


class Section(models.Model):
    name = models.CharField(max_length=100, verbose_name="Section name")

    class Meta:
        verbose_name = "Section"


class Area(models.Model):
    risk_choices = (
        ("High", "high"),
        ("Medium", "medium"),
        ("Low", "low"),
    )
    area_name = models.CharField(max_length=100, verbose_name="Area name")
    expected_controls = models.CharField(max_length=500, verbose_name="Expected Controls")
    findings = models.CharField(max_length=100, verbose_name="Findings")
    risk = models.CharField(max_length=50, choices=risk_choices, verbose_name="Risk Severity")
    recommendation = models.CharField(max_length=500, verbose_name="Recommendation")
    comment = models.CharField(max_length=500, verbose_name="Management Comment")
    implementation_date = models.DateField(auto_now_add=False, verbose_name="Target Implementation Date")
    section = models.ForeignKey("Section", verbose_name="Section", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Area"


class Template(models.Model):
    name = models.CharField(max_length=100, verbose_name="Template Name")
    regional_office = models.ForeignKey("RO", verbose_name="Regional Office", on_delete=models.CASCADE)
    country_office = models.ForeignKey("CO", verbose_name="Country Office", on_delete=models.CASCADE)
    business_unit = models.ForeignKey("BU", verbose_name="Business Unit", on_delete=models.CASCADE)
    sections = models.ManyToManyField("Section")
    areas = models.ManyToManyField("Area")

    class Meta:
        verbose_name = "Template"