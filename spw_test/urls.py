from django.urls import re_path

from . import views
from base import lookups as lookups_view

app_name = "spw_test"

urlpatterns = [
    re_path(r"^hello/$", views.hello, name="hello"),

    re_path(r"^employees/$", views.employees, name="employees"),
    re_path(r"^employee_search/$", views.employee_search, name="employee_search"),
    re_path(r"^employee/(\d+)/$", views.employee, name="employee"),
    re_path(r"^employee_save/$", views.employee_save, name="employee_save"),
    re_path(r"^employee_delete/$", views.employee_delete, name="employee_delete"),

    re_path(r"^employees_address/$", views.employees_address, name="employees_address"),
    re_path(r"^employees_address/(\d+)/$", views.employees_address, name="employees_address"),
    re_path(r"^employee_address_search/$", views.employee_address_search, name="employee_address_search"),
    re_path(r"^employee_address/(\d+)/$", views.employee_address, name="employee_address"),
    re_path(r"^employee_address_save/$", views.employee_address_save, name="employee_address_save"),
    re_path(r"^employee_address_delete/$", views.employee_address_delete, name="employee_address_delete"),

    re_path(r"^employees_leave/$", views.employees_leave, name="employees_leave"),
    re_path(r"^employees_leave/(\d+)/$", views.employees_leave, name="employees_leave"),
    re_path(r"^employee_leave_search/$", views.employee_leave_search, name="employee_leave_search"),
    re_path(r"^employee_leave/(\d+)/$", views.employee_leave, name="employee_leave"),
    re_path(r"^employee_leave_save/$", views.employee_leave_save, name="employee_leave_save"),
    re_path(r"^employee_leave_delete/$", views.employee_leave_delete, name="employee_leave_delete"),
    
    re_path(r"^employee_leave_status/$", views.employee_leave_status, name="employee_leave_status"),
    re_path(r"^employees_leaves_master/$", views.employees_leaves_master, name="employees_leaves_master"),
    re_path(r"^employees_leaves_master_search/$", views.employees_leaves_master_search, name="employees_leaves_master_search"),

    re_path(r"^salary_slip/(\d+)/$", views.salary_slip, name="salary_slip"),
    re_path(r"^salary_slip_download/$", views.salary_slip_download, name="salary_slip_download"),


    re_path(r"^lookups/([^/]+)/$", lookups_view.lookups, name="lookups"),
]