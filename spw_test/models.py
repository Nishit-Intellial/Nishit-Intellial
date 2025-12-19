from __future__ import unicode_literals
from django.db import models


class EmployeeDesignation(models.Model):
    designation = models.CharField(max_length=255, null=False, verbose_name="Designation")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.designation


class Employee(models.Model):
    first_name = models.CharField(max_length=50, null=False, verbose_name="First name")
    last_name = models.CharField(max_length=150, verbose_name="Last name")
    mobile_num = models.CharField(max_length=15, verbose_name="Mobile number")
    designation = models.ForeignKey(EmployeeDesignation, on_delete=models.CASCADE)

    basic_salary = models.DecimalField(max_digits=15, decimal_places=2, default=100000.0, verbose_name="Basic Salary")
    special_allowance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, verbose_name="Special Allowance")
    other_allowance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, verbose_name="Other Allowance")
    other_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, verbose_name="Other Deduction")

    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Address(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    address = models.CharField(max_length=80, null=False, verbose_name="Address")
    district = models.CharField(max_length=80, null=False, verbose_name="District")
    state = models.CharField(max_length=80, null=False, verbose_name="State")
    country = models.CharField(max_length=80, null=False, verbose_name="Country")
    pin_code = models.IntegerField(blank=True, verbose_name="Pin code")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} | {self.district}, {self.state}"


class LeaveType(models.Model):
    LEAVE_CHOICES = [
        ('LWP', 'LWP'),
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
    ]
    leave_name = models.CharField(max_length=20, choices=LEAVE_CHOICES)
    code = models.CharField(max_length=2, verbose_name="Code")
    count = models.IntegerField(blank=True, verbose_name="Count")
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.leave_name} ({self.code})"


class EmployeeLeave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    taken_leave = models.IntegerField(blank=True, verbose_name="Taken Leave")
    allocated = models.IntegerField(blank=True, verbose_name="Allocated")
    balance = models.IntegerField(blank=True, verbose_name="Balance")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} | {self.leave_type} | Balance: {self.balance}"


class LeaveDuration(models.Model):
    duration = models.CharField(max_length=10, null=False, verbose_name="Duration")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.duration


class EmployeeLeaveMaster(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    leave_start_date = models.DateField(verbose_name="Leave Start Date")
    leave_end_date = models.DateField(verbose_name="Leave End Date")
    reason = models.TextField(verbose_name="Reason for Leave", blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name="Leave Duration")
    leave_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} | {self.leave_type} | {self.leave_status}"

