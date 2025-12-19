from django.contrib import admin
from .models import (
    Employee, LeaveType, EmployeeDesignation, 
    EmployeeLeaveMaster, EmployeeLeave, LeaveDuration, Address
)


# ------------------------------
# EmployeeDesignation Admin
# ------------------------------
@admin.register(EmployeeDesignation)
class EmployeeDesignationAdmin(admin.ModelAdmin):
    list_display = ('designation', 'is_deleted')
    search_fields = ('designation',)
    list_filter = ('is_deleted',)


# ------------------------------
# Employee Admin
# ------------------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'get_designation', 
        'mobile_num', 'basic_salary', 'special_allowance', 
        'other_allowance', 'other_deduction', 'is_deleted'
    )
    search_fields = (
        'first_name', 'last_name', 'mobile_num', 
        'designation__designation'
    )
    list_filter = ('designation', 'is_deleted')

    def get_designation(self, obj):
        return obj.designation.designation
    get_designation.short_description = 'Designation'


# ------------------------------
# Address Admin
# ------------------------------
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('employee', 'address', 'district', 'state', 'country', 'pin_code', 'is_deleted')
    search_fields = ('employee__first_name', 'employee__last_name', 'district', 'state', 'country')
    list_filter = ('state', 'country', 'is_deleted')


# ------------------------------
# LeaveType Admin
# ------------------------------
@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('leave_name', 'code', 'count', 'is_deleted', 'created_on')
    search_fields = ('leave_name', 'code')
    list_filter = ('is_deleted',)


# ------------------------------
# EmployeeLeave Admin
# ------------------------------
@admin.register(EmployeeLeave)
class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'taken_leave', 'allocated', 'balance', 'is_deleted')
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type__leave_name')
    list_filter = ('leave_type', 'is_deleted')


# ------------------------------
# LeaveDuration Admin
# ------------------------------
@admin.register(LeaveDuration)
class LeaveDurationAdmin(admin.ModelAdmin):
    list_display = ('duration', 'is_deleted')
    search_fields = ('duration',)
    list_filter = ('is_deleted',)


# ------------------------------
# EmployeeLeaveMaster Admin
# ------------------------------
@admin.register(EmployeeLeaveMaster)
class EmployeeLeaveMasterAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'leave_start_date', 'leave_end_date', 'duration', 'leave_status', 'is_deleted')
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type__leave_name', 'leave_status')
    list_filter = ('leave_type', 'leave_status', 'is_deleted')
