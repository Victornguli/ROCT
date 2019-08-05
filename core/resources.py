from import_export import resources
from .models import Oversight

class OversightResource(resources.ModelResource):
    class Meta:
        model = Oversight