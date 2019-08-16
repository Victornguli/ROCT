"""ROCT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import filterTemplates, loadTemplate, editTemplate, defineTemplate, startOversight, ongoingOversight, editOversight, renderAreaForm, export, updateInline, filterFollowUp, submitOversight, editFollowUp
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.reports ,name="reports"),
    path('templates/', filterTemplates ,name="filter_templates"),
    path('load/<int:template_id>',loadTemplate,name="load_template"),
    path('start/<int:template_id>',startOversight,name="start"),
    path('define', defineTemplate ,name="define_template"),
    path('edit/<int:template_id>',editTemplate,name="edit_template"),
    path('oversights/',ongoingOversight,name="oversights"),
    path('follow-up/',filterFollowUp,name="follow_up"),
    path('edit-follow-up/<int:oversight_id>',editFollowUp,name="edit_follow_up"),
    path('ajax/edit/',views.edit_oversight_ajax,name="edit_area"),    
    path('submit-oversight/<int:oversight_id>',submitOversight,name="submit_oversight"),
    path('edit-oversight/<int:oversight_id>',editOversight,name="edit_oversight"),
    path('ajax/area_form',renderAreaForm ,name="render_area"),
    path('edit/update_inline',updateInline ,name="update_inline"),
    path('close/<int:oversight_id>',views.close_oversight ,name="close"),
    path('closed-oversights/',views.closed_oversights ,name="closed_oversights"),
    path('view-closed/<int:oversight_id>',views.view_closed_oversight ,name="view_closed"),
    path('export/<int:oversight_id>',export ,name="export"),

]
