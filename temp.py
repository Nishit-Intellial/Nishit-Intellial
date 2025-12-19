import os
import django
import json
import logging
from django.shortcuts import render
from django.http import HttpResponse
from base.models import AppResponse
from django.db.models import Q,F
from decimal import Decimal
from datetime import datetime,timedelta
from django.utils import timezone
from calendar import monthrange
from django.template.loader import render_to_string
# 🔹 SET YOUR PROJECT SETTINGS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment.settings')

django.setup()

from spw_test.models import Employee, LeaveType, EmployeeLeave


def add_lwp_leave():
    month_date = datetime.today()
    month_str = month_date.strftime("%Y-%m")
    total_days = monthrange(month_date.year, month_date.month)
    print(total_days)
    
if __name__ == "__main__":
    add_lwp_leave()
