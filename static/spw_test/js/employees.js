function employeesInit() {
  sparrow.registerCtrl(
    "employeesCtrl",
    function (
      $scope,
      $rootScope,
      $route,
      $routeParams,
      $compile,
      DTOptionsBuilder,
      DTColumnBuilder,
      $templateCache,
      ModalService
    ) {
      var config = {
        pageTitle: "Employees",
        topActionbar: {
            add: {
                url: '/#/spw_test/employee/',
            },
            edit: {
                url: '/#/spw_test/employee/',
            },
            delete: {
                url: '/spw_test/employee_delete/',
            },
            extra: [
              {
                id: "salary_slip",
                multiselect: false,
                noselect: false,
                function: function () {
                  $scope.generateSalarySlip();
                }
              },
            ]
        },
        listing: [
          {
            index: 1,
            url: "/spw_test/employee_search/",
            crud: true,
            search: {
                params: [
                    { key: "first_name", name: "First name" },
                    { key: "last_name", name: "Last name" },
                    { key: "mobile_num", name: "Mobile number"},
                    { key: "designation", name: "Designation"}
                ],
            },
            columns: [
              {
                name: "first_name",
                title: "First name",
                renderWith: function(data, type, full, meta) {
                    return `<a href="/#/spw_test/employee/${full.id}">${data}</a>`
                }
              },
              {
                name: "last_name",
                title: "Last name",
              },
              {
                name: "designation",
                title: "Designation",
              },
              {
                name: "mobile_num",
                title: "Mobile number",
              },
              
              {
                name: "address_emp",
                title: "Address",
                renderWith: function (data, type, full, meta) {
                    return `<a ng-click="openEmployeeAddress(${full.id})" id="employee_id">View Address</a>`
                },
                sort: false
              },

             
           
            ],
          },
        ],
      };

      
       $scope.generateSalarySlip = function() {
        
            
            var employeeId = $scope['selected1'] && $scope['selected1'][0];
  
            if (!employeeId) {
              sparrow.showMessage('appMsg', sparrow.MsgType.Error, 'Please select a Employee to generate Salary Slip.', 5);
              return;
            }
  
            var url = "/#/spw_test/salary_slip/" + employeeId + "/";  
            window.location =
              url
            // var postData = {};
  
            // sparrow.post(url, postData, true, function(response) {
            //   if ( sparrow.MsgType.Error) {
            //       sparrow.showMessage('appMsg', sparrow.MsgType.Error, 'Failed to approve the leave.', 5);
            //   } else {
            //       $scope.reloadData(1);
            //       sparrow.showMessage('appMsg', sparrow.MsgType.Success, 'Leave approved successfully.', 5);
            //   }
            // });
          
      };

      $scope.openEmployeeAddress = function(empId) {
          url = `/iframe_index/#/spw_test/employees_address/${empId}`
          $scope.onEditLink(url, "Employee Address", null, true, 1, false);
      }

      $scope.openEmployeeLeave = function(empId) {
          url = `/iframe_index/#/spw_test/employees_leave/${empId}`
          $scope.onEditLink(url, "Employee Leave", null, true, 1, false);
      }



      $scope.confirmDelete = function(employeeId) {
        if (confirm("Are you sure you want to delete this employee?")) {
          sparrow.onDelete(employeeId);
        }
      };
      $scope.onAddressView = function(employeeId) {
        window.location.href = "/#/spw_test/employees_address/" + employeeId + "/";
      };

      sparrow.setup(
        $scope,
        $rootScope,
        $route,
        $compile,
        DTOptionsBuilder,
        DTColumnBuilder,
        $templateCache,
        config,
        ModalService
      );
    }
  );
}

employeesInit();