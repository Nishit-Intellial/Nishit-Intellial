function employeeAddressInit(data) {
  sparrow.registerCtrl(
    "employeeLeaveCtrl",
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
        pageTitle: "Employee Leave",
        topActionbar: {},
      };

        setAutoLookup("id_employee", '/spw_test/lookups/employee/', '')
        setAutoLookup("id_leavetype", '/spw_test/lookups/leavetype/', '')


        $scope.saveEmployeeLeave = function () {
            
            var employee = $("#hid_employee").val();
                if (!employee) {
                    console.log("error")
                    sparrow.showMessage("appMsg", sparrow.MsgType.Error, "Employee should be selected", 5);
                    return;
                }
            var leave_type = $("#hid_leavetype").val();
                if (!leave_type) {
                    console.log("error")
                    sparrow.showMessage("appMsg", sparrow.MsgType.Error, "Leave Type should be selected", 5);
                    return;
                } 
            

            sparrow.postForm(
                {
                    employeeleave_id: $routeParams.id,
                },
                $("#frmSaveEmployeeLeave"),
                $scope,
                function () {
                     sparrow.redirect("#/spw_test/employees_leaves_master");
                }
            );
        };

        $scope.onClose = function () {
            sparrow.redirect("#/spw_test/employees_leaves_master");
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
employeeAddressInit();