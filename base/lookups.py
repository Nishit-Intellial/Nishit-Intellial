from itertools import chain
from django.db.models import Q
from django.http import HttpResponse
from base.models import (
    AppResponse,
)
from base.util import Util
from spw_test.models import Employee,LeaveType,EmployeeDesignation


class Lookup:
    def __init__(
        self,
        model_name,
        columns=None,
        query=None,
        search_value="",
        length=None,
        order_by=None,
    ):
        self.model_name = model_name
        self.data_order = order_by
        search_value = search_value.strip()
        if length is None:
            length = 10
        if query is None:
            query = Q()
        if search_value != "" and model_name != "UserProfile":
            # query = Q()
            query.add(Q(name__istartswith=search_value), query.connector)
        if search_value != "" and model_name == "OperationMaster":
            query = Q()
            query.add(
                Q(name__icontains=search_value, is_deleted=False, is_active=True),
                query.connector,
            )
        if search_value != "" and model_name == "UserProfile":
            # query = Q()
            query.add(
                Q(user__first_name__icontains=search_value) | Q(user__last_name__icontains=search_value),
                query.connector,
            )
        if columns is None:
            columns = ["id", "name"]
        self.query = query
        self.columns = columns
        self.search_value = search_value
        self.length = length

    def get_data(self):
        model_instance = globals()[self.model_name]
        data = None
        if self.search_value == "":

            data = Util.get_cache("public", "lookup_default_data_" + self.model_name)
            # if data is not None:

        if data is None and self.search_value == "":
            if self.model_name in ["Routing", "OperationMaster"]:
                if self.data_order is not None:
                    data = model_instance.objects.filter(self.query).order_by(self.data_order).values(*self.columns)
                else:
                    data = model_instance.objects.filter(self.query).values(*self.columns)
            else:
                if self.data_order is not None:
                    data = model_instance.objects.filter(self.query).order_by(self.data_order).values(*self.columns)[: self.length]
                else:
                    data = model_instance.objects.filter(self.query).values(*self.columns)[: self.length]
            Util.set_cache("public", "lookup_default_data_" + self.model_name, data)

        if self.query != "" and data is None:
            data = Util.get_cache("public", "lookup_default_data_" + self.model_name)
            comparision_field = "user__first_name" if self.model_name == "UserProfile" else "name"
            if self.search_value in [text[comparision_field] for text in data] and self.search_value != "":
                data = Util.get_cache("public", "lookup_default_data_" + self.model_name)

            else:
                if self.model_name in ["Routing", "OperationMaster"]:
                    data = model_instance.objects.filter(self.query).values(*self.columns)
                else:
                    data = model_instance.objects.filter(self.query).values(*self.columns)[: self.length]

        return data

    def get_response(self):
        items = self.get_data()
        response = []
        for item in items:
            response.append(item)
        return response

    def get_seleted_data(self, selectedID):
        response = []
        model_instance = globals()[self.model_name]
        cache_data = Util.get_cache("public", "lookup_default_data_" + self.model_name)
        if cache_data is not None:
            stored_ids = []
            for data_id in cache_data:
                stored_ids.append(data_id["id"])
            if int(selectedID) in stored_ids:
                data = Util.get_cache("public", "lookup_default_data_" + self.model_name)

            else:
                if self.model_name in ["Routing", "OperationMaster"]:
                    db_data = model_instance.objects.filter(id=selectedID).values(*self.columns)
                else:
                    db_data = model_instance.objects.filter(id=selectedID).values(*self.columns)[: self.length]
                if len(cache_data) != 0:
                    data = list(chain(db_data, cache_data))
                    if self.model_name in ["Routing", "OperationMaster"]:
                        data = data
                    else:
                        data = data[:10]
                    Util.set_cache("public", "lookup_default_data_" + self.model_name, data)
        else:
            if self.model_name in ["Routing", "OperationMaster"]:
                data = model_instance.objects.filter(id=selectedID).values(*self.columns)
            else:
                data = model_instance.objects.filter(id=selectedID).values(*self.columns)[: self.length]
        for item in data:
            response.append(item)
        return response



def lookups(request, model):
    response = []
    q = request.POST.get("query")
    bid = request.POST.get("bid")  # base id passed when dropdown is dependent on base field
    onfocus = request.POST.get("onfocus")
    selectedId = request.POST.get("id", False)
    if selectedId == "" and q == "" and not onfocus:
        response.append({"name": "", "id": ""})
        return HttpResponse(AppResponse.get(response), content_type="json")

    selectedIds = []
    if selectedId and selectedId.find(","):
        selectedIds = [int(x) for x in selectedId.split(",")]


    if model == "employee":
        employees = Employee.objects.filter(is_deleted=False)
        response = []

        for emp in employees:
            response.append({
                "id": emp.id,
                "name": f"{emp.first_name} {emp.last_name}",
            })
        
        return HttpResponse(AppResponse.get(response), content_type="json")
    
    if model == "leavetype":
        leavetypes = LeaveType.objects.filter(is_deleted=False)
        response = []

        for leavetype in leavetypes:
            response.append({
                "id": leavetype.id,
                "name": leavetype.leave_name,
            })
        
        return HttpResponse(AppResponse.get(response), content_type="json")
    
    if model == "designation":
        designations = EmployeeDesignation.objects.filter(is_deleted=False)
        response = []

        for designation in designations:
            response.append({
                "id": designation.id,
                "name": designation.designation,
            })
        
        return HttpResponse(AppResponse.get(response), content_type="json")

