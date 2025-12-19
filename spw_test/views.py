import json
import logging
from django.shortcuts import render
from base.util import Util
from .models import Employee,Address,EmployeeLeave,LeaveType,EmployeeLeaveMaster,EmployeeDesignation
from django.http import HttpResponse
from base.models import AppResponse
from django.db.models import Q,F
from decimal import Decimal
from datetime import datetime,timedelta,date
from django.utils import timezone
from calendar import monthrange
from django.template.loader import render_to_string
import pdfkit # type: ignore

def hello(request):
    return render(request,"spw_test/hello.html")


def employees(request):
    return render(request,"spw_test/employees.html")


def employee_search(request):
    try:
        """
        request object contains useful information like
        - sorting column,
        - length of data, start position - Which is useful for pagination
        - Custom posted data

        get_post_data function rearrange all above data in assign back to request.POST object
        """
        request.POST = Util.get_post_data(request)

        query = Q(is_deleted=False)

        if request.POST.get("first_name"):
            query &= Q(first_name__icontains=request.POST.get("first_name"))
        if request.POST.get("last_name"):
            query &= Q(last_name__icontains=request.POST.get("last_name"))
        if request.POST.get("mobile_num"):
            query &= Q(mobile_num__icontains=request.POST.get("mobile_num"))
        if request.POST.get("designation"):
            query &= Q(designation__designation__icontains=request.POST.get("designation"))
        
        """
          start and length used for pagination
        """
        start = int(request.POST["start"])
        length = int(request.POST["length"])

        #Get the default sorting column
        sort_col = Util.get_sort_column(request.POST)

        # recordsTotal is sent back in response. Based on this pagination numbers are generated
        recordsTotal = Employee.objects.filter(query).count()

        """
          [start : (start + length)] - This is for pagination
          sort_col - Sorted data based on this column
        """

        all_employee = Employee.objects.filter(query).order_by(sort_col)[start:(start + length)]

        response = {
            "draw": request.POST["draw"],
            "recordsTotal": recordsTotal,
            "recordsFiltered": recordsTotal,
            "data": [],
        }

        for emp in all_employee:
            response["data"].append({
                "id": emp.id,              
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "mobile_num": emp.mobile_num,   
                "designation":emp.designation.designation
            })


        return HttpResponse(AppResponse.get(response), content_type="json")
    except Exception as e:
        logging.exception(e)
        print(f"error : {e}")


def employee(request, employee_id):
    try:
        employee = None
        if employee_id != "0":
            employee = Employee.objects.get(id=employee_id)
            
        return render(request, "spw_test/employee.html", {"employee": employee})
    except Exception as e:
        logging.exception(e)
        print(f"error : {e}")


# def employee_save(request):
#     first_name = request.POST.get("first_name")
#     print("first_name", first_name)
#     last_name = request.POST.get("last_name")
#     print("last_name", last_name)
#     mobile_num = request.POST.get("mobile_num")
#     print("mobile_num", mobile_num)
#     address = request.POST.get("address")
#     print("address", address)
#     pin_code = request.POST.get("pin_code")
#     print("pin_code", pin_code)

#     employee = Employee.objects.create(first_name=first_name, last_name=last_name, mobile_num=mobile_num, address=address, pin_code=pin_code)
#     print("employee", employee)

#     response = {"code": 1, "msg": "Employee saved."}
#     return HttpResponse(AppResponse.get(response), content_type="json")


def employee_save(request):
    try:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile_num = request.POST.get("mobile_num")
        employee_id = request.POST.get("employee_id")
        designation = EmployeeDesignation.objects.get(id=request.POST.get("designation"))
        basic_salary = Decimal(request.POST.get("basic_salary"))
        special_allowance = Decimal(request.POST.get("special_allowance") or 0.0)
        other_allowance = Decimal(request.POST.get("other_allowance") or 0.0)
        other_deduction = Decimal(request.POST.get("other_deduction") or 0.0)

        

        employee = None
        if employee_id != "0":
            employee = Employee.objects.get(id=employee_id)
            employee.first_name = first_name
            employee.last_name = last_name
            employee.mobile_num = mobile_num
            employee.designation = designation
            employee.basic_salary = basic_salary
            employee.special_allowance = special_allowance
            employee.other_allowance = other_allowance
            employee.other_deduction = other_deduction
            employee.save()
           
        else:
            employee = Employee.objects.create(
                first_name=first_name, 
                last_name=last_name, 
                mobile_num=mobile_num,    
                designation = designation,
                basic_salary = basic_salary,
                special_allowance = special_allowance,
                other_allowance = other_allowance,
                other_deduction = other_deduction,
                )
            
            sick = LeaveType.objects.get(leave_name="Sick Leave")
            casual = LeaveType.objects.get(leave_name="Casual Leave")
            lwp = LeaveType.objects.get(leave_name="LWP")
            
            EmployeeLeave.objects.create(
                employee=employee,
                leave_type=sick,
                taken_leave=0,
                allocated=sick.count,
                balance=sick.count,
            )
            EmployeeLeave.objects.create(
                employee=employee,
                leave_type=casual,
                taken_leave=0,
                allocated=casual.count,
                balance=casual.count,
            )
            EmployeeLeave.objects.create(
                employee=employee,
                leave_type=lwp,
                taken_leave=0,
                allocated=casual.count,
                balance=casual.count,
            )

        response = {"code": 1, "msg": "Employee saved."}
        return HttpResponse(AppResponse.get(response), content_type="json")
    except Exception as e:
        logging.exception(e)
        print(f"error : {e}")


def employee_delete(request):
    try:
        post_ids = request.POST.get("ids")
        ids = post_ids.split(",")
        Employee.objects.filter(id__in=ids).update(is_deleted=True)

        response = {"code": 1, "msg": "Employee deleted." }
        return HttpResponse(AppResponse.get(response), content_type="json")
    except Exception as e:
        logging.exception(e)
        return HttpResponse(AppResponse.get({"error": str(e)}), content_type="application/json")
    

def employees_address(request, employee_id=None):
    try:
        employee_id = int(employee_id) if employee_id else 0

        return render(request, "spw_test/employees_address.html", {"employee_id": employee_id})
    except Exception as e:
        logging.exception(e)
        return HttpResponse("Internal Server Error", status=500)


def employee_address_search(request):
    try:
        """
        request object contains useful information like
        - sorting column,
        - length of data, start position - Which is useful for pagination
        - Custom posted data

        get_post_data function rearrange all above data in assign back to request.POST object
        """
        request.POST = Util.get_post_data(request)

        query = Q(is_deleted=False)

        if request.POST.get("employee"):
            emp =  request.POST.get("employee")
            if " " in emp: 
                first, last = emp.split(" ", 1)
                query &= Q(employee__first_name__icontains=first) & Q(employee__last_name__icontains=last)
            else:  
                query &= Q(employee__first_name__icontains=emp) | Q(employee__last_name__icontains=emp)
        if request.POST.get("address"):
            query &= Q(address__icontains=request.POST.get("address"))
        if request.POST.get("district"):
            query &= Q(district__icontains=request.POST.get("district"))
        if request.POST.get("state"):
            query &= Q(state__icontains=request.POST.get("state"))
        if request.POST.get("country"):
            query &= Q(country__icontains=request.POST.get("country"))
        if request.POST.get("pin_code"):
            query &= Q(pin_code__icontains=request.POST.get("pin_code"))

        """
          start and length used for pagination
        """

        start = int(request.POST["start"])
        length = int(request.POST["length"])

        #Get the default sorting column
        sort_col = Util.get_sort_column(request.POST)

        # recordsTotal is sent back in response. Based on this pagination numbers are generated
        recordsTotal = Address.objects.filter(query).count()

        employee_id = request.POST.get("employeeId")
        try:
            employee_id = int(employee_id) if employee_id else 0
        except:
            employee_id = 0

        """
          [start : (start + length)] - This is for pagination
          sort_col - Sorted data based on this column
        """
        if(employee_id != 0):
            all_addr = Address.objects.filter(query,employee_id=employee_id,employee__is_deleted=False).order_by(sort_col)[start:(start + length)]
        else:
            all_addr = Address.objects.filter(query, employee__is_deleted=False)

        
        response = {
            "draw": request.POST["draw"],
            "recordsTotal": recordsTotal,
            "recordsFiltered": recordsTotal,
            "data": [],
        }


        for addr in all_addr:
            response["data"].append({
                "id":addr.id,
                "employee":f"{addr.employee.first_name} {addr.employee.last_name}",
                "address" :addr.address,
                "state" :addr.state,
                "country" :addr.country,
                "pin_code" :addr.pin_code,
                "district" :addr.district,
                
            })

        return HttpResponse(AppResponse.get(response), content_type="json")
    except Exception as e:
        logging.exception(e)
        print(f"error : {e}")


def employee_address(request, address_id):
    try:
        address_obj = None
        selected_employee_id = -1
        if address_id != "0":
            address_obj = Address.objects.get(id=address_id )
            selected_employee_id = address_obj.employee.id

        employees = Employee.objects.filter( is_deleted=False)

        return render(
            request,
            "spw_test/employee_address.html",
            {
                "address": address_obj,
                "employees": employees,
                "selected_employee_id":selected_employee_id
            }
        )

    except Exception as e:
        print("Error:", e)
        return HttpResponse("Error loading address", status=500)


def employee_address_save(request):
    try:
        
        address_id = request.POST.get("address_id")
        employee_id = request.POST.get("employee")
        address_str = request.POST.get("address")
        pin_code = request.POST.get("pin_code")
        district = request.POST.get("district")
        state = request.POST.get("state")
        country = request.POST.get("country")

        address = None
        if address_id != "0":

            address = Address.objects.get(id=address_id)
            address.employee_id=employee_id
            address.address = address_str
            address.pin_code = pin_code
            address.district = district
            address.state = state
            address.country = country

            address.save()

        else:
            address = Address.objects.create(employee_id=employee_id,address=address_str,pin_code=pin_code,state=state,district=district,country=country)
        response = {"code": 1, "msg": "Employee address saved."}
        return HttpResponse(AppResponse.get(response), content_type="json")
    
    except Exception as e:
        logging.exception(e)
        print(f"error : {e}")


def employee_address_delete(request):
    try:
        post_ids = request.POST.get("ids")
        ids = post_ids.split(",")
        
        Address.objects.filter(id__in=ids).update(is_deleted=True)

        response = {"code": 1, "msg": "Employee Address deleted." }
        return HttpResponse(AppResponse.get(response), content_type="json")
    except Exception as e:
        logging.exception(e)
        return HttpResponse(AppResponse.get({"error": str(e)}), content_type="application/json")
    

# Leaves
def employees_leave(request, employee_id=None):
    try:
        employee_id = int(employee_id) if employee_id else 0

        return render(request, "spw_test/employees_leave.html", {"employee_id": employee_id})
    except Exception as e:
        logging.exception(e)
        return HttpResponse("Internal Server Error", status=500)


def employee_leave_search(request):
    try:
        request.POST = Util.get_post_data(request)

        query = Q(is_deleted=False)

        if request.POST.get("employee"):
            emp = request.POST.get("employee")
            if " " in emp: 
                first, last = emp.split(" ", 1)
                query &= Q(employee__first_name__icontains=first) & Q(employee__last_name__icontains=last)
            else:  
                query &= Q(employee__first_name__icontains=emp) | Q(employee__last_name__icontains=emp)
        if request.POST.get("leave_type"):
            query &= Q(leave_type__leave_name__icontains=request.POST.get("leave_type"))
        if request.POST.get("leave_taken"):
            query &= Q(taken_leave__icontains=request.POST.get("leave_taken"))
        if request.POST.get("allocated"):
            query &= Q(allocated__icontains=request.POST.get("allocated"))
        if request.POST.get("balance"):
            query &= Q(balance__icontains=request.POST.get("balance"))

        start = int(request.POST["start"])
        length = int(request.POST["length"])
        sort_col = Util.get_sort_column(request.POST)

        employee_id = int(request.POST.get("employeeId") or 0)

        if employee_id:
            all_data = EmployeeLeave.objects.filter(query, employee_id=employee_id,employee__is_deleted=False).order_by(sort_col)
        else:
            all_data = EmployeeLeave.objects.filter(query,employee__is_deleted=False).order_by(sort_col)

        recordsTotal = all_data.count()

        page_data = all_data[start:start + length]

        response = {
            "draw": request.POST["draw"],
            "recordsTotal": recordsTotal,
            "recordsFiltered": recordsTotal,
            "data": [],
        }

        for item in page_data:
            response["data"].append({
                "id": item.id,
                "employee": f"{item.employee.first_name} {item.employee.last_name}",
                "leave_type": item.leave_type.leave_name,
                "taken_leave": item.taken_leave,
                "allocated": item.allocated,
                "balance": item.balance,
            })

        return HttpResponse(AppResponse.get(response), content_type="json")

    except Exception as e:
        logging.exception(e)
        return HttpResponse("ERROR", status=500)


def employee_leave(request, employeeleave_id):
    try:
        leave_obj = None
        selected_employee_id = -1
        selected_leave_type_id = -1

        if employeeleave_id != "0":
            leave_obj = EmployeeLeaveMaster.objects.get(id=employeeleave_id)
            selected_employee_id = leave_obj.employee_id
            selected_leave_type_id = leave_obj.leave_type_id

        employees = Employee.objects.filter(is_deleted=False)
        leave_types = LeaveType.objects.filter(is_deleted=False)

        return render(
            request,
            "spw_test/employee_leave.html",
            {
                "employee_leave": leave_obj,
                "employees": employees,
                "leave_types": leave_types,
                "selected_employee_id": selected_employee_id,
                "selected_leave_type_id": selected_leave_type_id,
            }
        )
    except Exception as e:
        logging.exception(e)
        return HttpResponse("Error loading employee leave", status=500)
    

def employee_leave_save(request):
    try:
        leave_id = request.POST.get("employeeleave_id")
        employee_id = request.POST.get("employee")
        leave_type_id = request.POST.get("leavetype")
        leave_start_date = request.POST.get("leave_start_date")
        leave_end_date = request.POST.get("leave_end_date")
        reason = request.POST.get("reason")
        leave_data_json = request.POST.get('leave_data') 

        leave_data = {}
        if leave_data_json:
            leave_data = json.loads(leave_data_json)

        leave_start_date = datetime.strptime(leave_start_date, "%Y-%m-%d").date()
        leave_end_date = datetime.strptime(leave_end_date, "%Y-%m-%d").date()
        current_date = leave_start_date

        leave_to_create = []

        continuous_start_date = None
        continuous_duration = Decimal(0.0)

        while current_date <= leave_end_date:
            current_duration = Decimal(leave_data.get(str(current_date), 0.0))

            existing_leaves = EmployeeLeaveMaster.objects.filter(
                employee_id=employee_id,
                is_deleted=False,
                leave_start_date__lte=current_date,
                leave_end_date__gte=current_date
            ).exclude(leave_status="Rejected")

            if existing_leaves.exists():
                total_existing_duration = sum(leave.duration for leave in existing_leaves)

                if total_existing_duration + current_duration > 1:
                    over_dates = []

                    while current_date <= leave_end_date:
                        current_duration = Decimal(leave_data.get(str(current_date), 0.0))

                        existing_leaves = EmployeeLeaveMaster.objects.filter(
                            employee_id=employee_id,
                            is_deleted=False,
                            leave_start_date__lte=current_date,
                            leave_end_date__gte=current_date
                        ).exclude(leave_status="Rejected")
                                    
                        if existing_leaves.exists():
                            total_existing_duration = sum(leave.duration for leave in existing_leaves)
                            if total_existing_duration + current_duration > 1:
                                over_dates.append(date_to_str(current_date))
                        
                        current_date += timedelta(days=1)

                    return HttpResponse(
                        AppResponse.get({
                            "code": 0,
                            "error": f"You cannot apply for more than 1 day of leave on {list_to_str(over_dates)[:-2]}."
                        }),
                        content_type="application/json"
                    )
                else:
                    leave_to_create.append({
                        "employee_id": employee_id,
                        "leave_type_id": leave_type_id,
                        "leave_start_date": current_date,
                        "leave_end_date": current_date,
                        "reason": reason,
                        "duration": current_duration
                    })
            else:
                if current_duration == 1:
                    if continuous_start_date is None:
                        continuous_start_date = current_date
                    continuous_duration += current_duration
                else:
                    
                    if continuous_start_date is not None:
                        leave_to_create.append({
                            "employee_id": employee_id,
                            "leave_type_id": leave_type_id,
                            "leave_start_date": continuous_start_date,
                            "leave_end_date": current_date - timedelta(days=1),  
                            "reason": reason,
                            "duration": continuous_duration
                        })

                    leave_to_create.append({
                        "employee_id": employee_id,
                        "leave_type_id": leave_type_id,
                        "leave_start_date": current_date,
                        "leave_end_date": current_date,
                        "reason": reason,
                        "duration": current_duration
                    })
                    continuous_start_date = None
                    continuous_duration = Decimal(0.0)

            current_date += timedelta(days=1)

        if continuous_start_date is not None:
            leave_to_create.append({
                "employee_id": employee_id,
                "leave_type_id": leave_type_id,
                "leave_start_date": continuous_start_date,
                "leave_end_date": current_date - timedelta(days=1),  
                "reason": reason,
                "duration": continuous_duration
            })

        if leave_to_create:
            EmployeeLeaveMaster.objects.bulk_create([
                EmployeeLeaveMaster(
                    employee_id=leave["employee_id"],
                    leave_type_id=leave["leave_type_id"],
                    leave_start_date=leave["leave_start_date"],
                    leave_end_date=leave["leave_end_date"],
                    reason=leave["reason"],
                    duration=leave["duration"]
                )
                for leave in leave_to_create
            ])

        return HttpResponse(
            AppResponse.get({"code": 1, "msg": "Employee Leave saved."}),
            content_type="json"
        )

    except Exception as e:
        logging.exception(e)
        return HttpResponse("Error", status=500)


def employee_leave_delete(request):
    try:
        post_ids = request.POST.get("ids")
        ids = post_ids.split(",")

        EmployeeLeaveMaster.objects.filter(id__in=ids).update(is_deleted=True)

        return HttpResponse(AppResponse.get({"code": 1, "msg": "Employee Leave Canceled."}),content_type="json")

    except Exception as e:
        logging.exception(e)
        return HttpResponse(AppResponse.get({"error": str(e)}), content_type="application/json")
    
# def employee_leave_delete(request):
#     try:
#         post_ids = request.POST.get("ids")
#         ids = post_ids.split(",")

#         leaves = EmployeeLeaveMaster.objects.filter(id__in=ids)
#         for leave in leaves:
#             if leave.leave_status == "Approved" and leave.leave_start_date > date.today():
#                 employee_leave = EmployeeLeave.objects.get(
#                     employee=leave.employee, leave_type=leave.leave_type
#                 )
#                 employee_leave.balance += leave.duration
#                 employee_leave.taken_leave -= leave.duration
#                 employee_leave.save()

#             leave.is_deleted = True
#             leave.save()

#         return HttpResponse(
#             AppResponse.get({"code": 1, "msg": "Employee Leave Canceled."}),
#             content_type="application/json"
#         )

#     except Exception as e:
#         logging.exception(e)
#         return HttpResponse(
#             AppResponse.get({"error": str(e)}),
#             content_type="application/json"
#         )



def employees_leaves_master(request):
    return render(request,"spw_test/employees_leaves_master.html")


def employees_leaves_master_search(request):
    try:
        request.POST = Util.get_post_data(request)

        query = Q(is_deleted=False)

        if request.POST.get("employee"):
            emp = request.POST.get("employee")
            if " " in emp: 
                first, last = emp.split(" ", 1)
                query &= Q(employee__first_name__icontains=first) & Q(employee__last_name__icontains=last)
            else:  
                query &= Q(employee__first_name__icontains=emp) | Q(employee__last_name__icontains=emp)
        if request.POST.get("leave_type"):
            query &= Q(leave_type__leave_name__icontains=request.POST.get("leave_type"))
        if request.POST.get("leave_range"):
            date_range=request.POST.get("leave_range")
            try :
                date_str_1, date_str_2 = date_range.split(" - ")
                leave_start_date = datetime.strptime(date_str_1, "%d/%m/%Y").strftime("%Y-%m-%d")
                leave_end_date = datetime.strptime(date_str_2, "%d/%m/%Y").strftime("%Y-%m-%d")
                query &= Q(leave_start_date__gte=leave_start_date)
                query &= Q(leave_end_date__lte=leave_end_date)
            except:
                return HttpResponse(AppResponse.get({"code": 0,"error": "Enter Dates in correct format."}), content_type="json")
            

        if request.POST.get("reason"):
            query &= Q(reason__icontains=request.POST.get("reason"))
        if request.POST.get("applied_on"):
            applied_on=request.POST.get("applied_on")
            try:
                date_str_1, date_str_2 = applied_on.split(" - ")
                applied_start_date = datetime.strptime(date_str_1, "%d/%m/%Y")
                applied_end_date = datetime.strptime(date_str_2, "%d/%m/%Y")
                applied_start_date_aware = timezone.make_aware(applied_start_date, timezone.get_current_timezone())
                applied_end_date = applied_end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                applied_end_date_aware = timezone.make_aware(applied_end_date, timezone.get_current_timezone())
                query &= Q(applied_on__gte=applied_start_date_aware)
                query &= Q(applied_on__lte=applied_end_date_aware)
            
            except:
                return HttpResponse(AppResponse.get({"code": 0, "error": "Enter Dates in correct format."}), content_type="json")


        if request.POST.get("leave_status"):
            query &= Q(leave_status__icontains=request.POST.get("leave_status"))
        
        start = int(request.POST["start"])
        length = int(request.POST["length"])
        sort_col = Util.get_sort_column(request.POST)

        employee_id = int(request.POST.get("employeeId") or 0)

        if employee_id:
            all_data = EmployeeLeaveMaster.objects.filter(query, employee_id=employee_id,employee__is_deleted=False).order_by(sort_col)
        else:
            all_data = EmployeeLeaveMaster.objects.filter(query,employee__is_deleted=False).order_by(sort_col)

        recordsTotal = all_data.count()

        page_data = all_data[start:start + length]

        response = {
            "draw": request.POST["draw"],
            "recordsTotal": recordsTotal,
            "recordsFiltered": recordsTotal,
            "data": [],
        }

        for item in page_data:
            response["data"].append({
                "id": item.id,
                "employee": f"{item.employee.first_name} {item.employee.last_name}",
                "leave_type": item.leave_type.leave_name,
                "leave_start_date":date_to_str(item.leave_start_date),
                "leave_end_date":date_to_str(item.leave_end_date),
                "reason":item.reason,
                "applied_on":date_to_str(item.applied_on),
                "leave_status":item.leave_status,
                "duration":float(item.duration)
            })

        return HttpResponse(AppResponse.get(response), content_type="json")

    except Exception as e:
        logging.exception(e)
        return HttpResponse("ERROR", status=500)


def employee_leave_status(request):
    status = request.POST.get("status")
    id = request.POST.get("leaveId")
    if(status=='approve'):
        try:

            employee_leave_master = EmployeeLeaveMaster.objects.get(id=id)
            balance = Decimal(EmployeeLeave.objects.get(employee=employee_leave_master.employee,leave_type=employee_leave_master.leave_type).balance)
            duration = employee_leave_master.duration

            if employee_leave_master.leave_status == 'Pending':
                if balance >= duration :
                    EmployeeLeave.objects.filter(
                        employee=employee_leave_master.employee,
                        leave_type=employee_leave_master.leave_type
                    ).update(
                        taken_leave=F('taken_leave') + duration,
                        balance=F('balance') - duration
                    )

                    EmployeeLeaveMaster.objects.filter(id=id).update(leave_status='Approved')

                    return HttpResponse(AppResponse.get({"code": 1,"msg": "Leave approved successfully"}), content_type="json")
                else:
                    return HttpResponse(AppResponse.get({"code": 0,"error": "Employee doesn't have enough balance"}), content_type="json")
            else:
                    return HttpResponse(AppResponse.get({"code": 0,"error": f"Leave status is already {employee_leave_master.leave_status}"}), content_type="json")
    
        except Exception as e:
            return HttpResponse(AppResponse.get({"code": 0,"error": "An error occurred while processing the leave request"}), content_type="json")
        
    elif(status=='reject'):
        try:
            employee_leave_master = EmployeeLeaveMaster.objects.get(id=id)

            if employee_leave_master.leave_status == 'Pending':
                EmployeeLeaveMaster.objects.filter(id=id).update(leave_status='Rejected')
                return HttpResponse(AppResponse.get({"code": 1,"msg": "Leave rejected successfully"}), content_type="json")
            else:
                return HttpResponse(AppResponse.get({"code": 0,"error":f"Leave status is already {employee_leave_master.leave_status}"}), content_type="json")
        
        except Exception as e:
            return HttpResponse(AppResponse.get({"code": 0,"error": "An error occurred while processing the leave request"}), content_type="json")


def salary_slip(request, id):
    try:
        employee = Employee.objects.get(id=id)
        month_str = request.POST.get("month") or request.GET.get("month")
        flag = month_str
        if month_str:
            month_date = datetime.strptime(month_str, "%Y-%m")
        else:
            month_date = datetime.today()
            month_str = month_date.strftime("%Y-%m")

        
        total_days = monthrange(month_date.year, month_date.month)[1]

        leaves = EmployeeLeaveMaster.objects.filter(
            employee=employee,
            leave_status="Approved",
            leave_start_date__year=month_date.year,
            leave_start_date__month=month_date.month
        )

        leaves_taken = sum(float(l.duration) for l in leaves)
        lwp_days = sum(
            float(l.duration) for l in leaves
            if l.leave_type.leave_name == "LWP"
        )

        basic = employee.basic_salary
        hra = basic * Decimal( 0.40)
        pf = basic * Decimal( 0.12)

        per_day_salary = basic / total_days
        lwp_deduction = per_day_salary * Decimal(lwp_days)

        gross_earnings = (
            basic +
            hra +
            employee.special_allowance +
            employee.other_allowance
        )

        total_deductions = (
            pf +
            lwp_deduction +
            employee.other_deduction + 200
        )

        net_salary = gross_earnings - total_deductions
                
        context = {
            "emp_id": id,
            "emp_name": f"{employee.first_name} {employee.last_name}",
            "emp_designation": employee.designation.designation,

            "selected_month": month_str,
            "total_days": int(total_days),
            "leaves_taken": float(leaves_taken),
            "lwp": float(lwp_days),

            "basic": float(basic),
            "hra": float(round(hra, 2)),
            "special": float(employee.special_allowance),
            "other_allowance": float(employee.other_allowance),
            "gross_earnings": float(round(gross_earnings, 2)),

            "pf": float(round(pf, 2)),
            "lwp_deduction": float(round(lwp_deduction, 2)),
            "other_deduction": float(employee.other_deduction),
            "total_deductions": float(round(total_deductions, 2)),
            "net_salary": "{:.2f}".format(round(net_salary, 2)),
            "professional_tax":float(200),

        }
        if flag:
            return HttpResponse(AppResponse.get(context), content_type="json")
        else:
            return render(request, "spw_test/salary_slip.html", context)
    except Exception as e:
        print(e)
        return HttpResponse(AppResponse.get({"code": 0,"error": "An error occurred while processing"}), content_type="json")


def salary_slip_download(request):
    try:
        if request.method == "POST":
            payload_raw = request.POST.get("payload")
            if not payload_raw:
                return HttpResponse(
                    AppResponse.get({"code": 0, "msg": "Payload missing"}),
                    content_type="application/json",
                    status=400
                )

            payload = json.loads(payload_raw)
            to_print = payload['selected_month']
            dt = datetime.strptime(payload['selected_month'], "%Y-%m")
            payload['selected_month'] = payload['month'] = dt.strftime("%B, %Y")

            html_string = render_to_string(
                "spw_test/salary_slip_download.html",
                payload
            )

            config = pdfkit.configuration(
                wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            )

            options = {
                "page-size": "A4",
                "encoding": "UTF-8",
                "enable-local-file-access": "",
                "quiet": ""
            }

            pdf_bytes = pdfkit.from_string(
                html_string,
                False,
                configuration=config,
                options=options
            )

            response = HttpResponse(pdf_bytes, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="salary_slip_{payload["emp_id"]}_{payload["emp_name"].split()[0]}_{payload["emp_name"].split()[1]}_{to_print}.pdf"'
            )
            return response
        return HttpResponse(AppResponse.get({"code": 0}),content_type="application/json")

    except Exception as e:
        return HttpResponse(AppResponse.get({"code": 0,"error": "An error occurred while processing"}), content_type="json")


def date_to_str(date):
    return date.strftime("%Y-%m-%d") if date else ""


def list_to_str(dates):
    dates_str = ""
    for d in dates:
        dates_str = dates_str + d +", "
    return dates_str
