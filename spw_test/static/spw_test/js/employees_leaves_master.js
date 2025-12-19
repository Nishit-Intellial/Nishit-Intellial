function employeesLeavesMasterInit() {
  sparrow.registerCtrl(
    "employeesLeavesMasterCtrl",
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
      
      var employeeId = $routeParams.id || 0;
      var baseUrl = (window !== window.top) ? '/iframe_index/#/' : '/#/';
      var config = {
        pageTitle: "Employees Leaves Master",
          topActionbar: {
            add: {
                url: '/#/spw_test/employee_leave/',
            },
            delete: {
                url: '/spw_test/employee_leave_delete/',
            },
            extra: [
              {
                id: "btnApprove",
                multiselect: false,
                noselect: false,
                function: function () {
                  $scope.onApprove();
                }
              },
              {
                id: "btnReject",
                multiselect: false,
                noselect: false,
                
                function: function () {
                  $scope.onReject();
                }
              }
            ]
          },
        listing: [
          {
            index: 1,
            url: "/spw_test/employees_leaves_master_search/",
            crud: true,
            postData: {
              employeeId: employeeId
            }, 
            search: {
                params: [
                    { key: "employee", name: "Employee" },
                    { key: "leave_type", name: "Leave Type" },
                    { key: "leave_range", name: "Leave Date Range", type: "datePicker"},
                    { key: "reason", name: "Reason" },
                    { key: "applied_on", name: "Applied On", type: "datePicker" },
                    { key: "leave_status", name: "Leave Status" },
                ],
            },
            columns: [
              {
                name: "employee",
                title: "Employee",
              },
              {
                name: "leave_type",
                title: "Leave Type",
              },
              {
                name: "leave_start_date",
                title: "Leave Start Date",
              },
              {
                name: "leave_end_date",
                title: "Leave End Date",
              },
              {
                name: "duration",
                title: "Duration (Day/s)",
              },
              {
                name: "reason",
                title: "Reason",
              },
              {
                name: "applied_on",
                title: "Applied On",
              },
              {
                name: "leave_status",
                title: "Leave Status",
              },
           
            ],
          },
        ],
      };

       

      $scope.onApprove = function() {
        sparrow.showConfirmDialog(
          ModalService,
          "Are you sure you want to approve leave?",
          "Approve Leave",
          function (confirmAction) {
            if (!confirmAction) {
              return;
            }
            
            var selectedLeaveId = $scope['selected1'] && $scope['selected1'][0];
  
            if (!selectedLeaveId) {
              sparrow.showMessage('appMsg', sparrow.MsgType.Error, 'Please select a leave request to approve.', 5);
              return;
            }
  
            var url = '/spw_test/employee_leave_status/';  
            var postData = { leaveId: selectedLeaveId ,status:"approve"};
  
            sparrow.post(url, postData, true, function(response) {
              if ( sparrow.MsgType.Error) {
                  sparrow.showMessage('appMsg', sparrow.MsgType.Error, 'Failed to approve the leave.', 5);
              } else {
                  $scope.reloadData(1);
                  sparrow.showMessage('appMsg', sparrow.MsgType.Success, 'Leave approved successfully.', 5);
              }
            });
          }
        );
      };

      $scope.onReject = function() {
        sparrow.showConfirmDialog(
          ModalService,
          "Are you sure you want to reject leave?",
          "Reject Leave",
          function (confirmAction) {
            if (!confirmAction) {
              return;
            }
            
            var selectedLeaveId = $scope['selected1'] && $scope['selected1'][0];

            if (!selectedLeaveId) {
              sparrow.showMessage('appMsg', sparrow.MsgType.Error, 'Please select a leave request to reject.', 5);
              return;
            }

            var url = '/spw_test/employee_leave_status/';  
            var postData = { leaveId: selectedLeaveId ,status:"reject"};

            sparrow.post(url, postData, true, function(response) {
                if ( sparrow.MsgType.Error) {
                  sparrow.showMessage('appMsg', sparrow.MsgType.Error, 'Failed to reject the leave.', 5);
                } else {
                  $scope.reloadData(1);
                  sparrow.showMessage('appMsg', sparrow.MsgType.Success, 'Leave Rejected successfully.', 5);
                }
            });
          }
        );
      };


      
      $scope.confirmDelete = function(employeeId) {
        sparrow.showConfirmDialog(
          ModalService,
          "Are you sure you want to Cancel this leave(s)?",
          "Cancel Leave",
          function (confirmAction) {
            if (!confirmAction) {
              return;
            }
            sparrow.onDelete(employeeId);
          }
        );
      };
      $

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

employeesLeavesMasterInit();