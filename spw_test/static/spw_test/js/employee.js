function employeeInit(data) {
  sparrow.registerCtrl(
    "employeeCtrl",
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
        pageTitle: "Employee",
        topActionbar: {},
      };

        
        setAutoLookup("id_designation", '/spw_test/lookups/designation/', '')

        $scope.saveEmployee = function () {
          var designation = $("#hid_designation").val();
          if (!designation ) {
              sparrow.showMessage("appMsg", sparrow.MsgType.Error, "Designation should be selected", 5);
              return;
          }
          sparrow.postForm({
              employee_id: $routeParams.id,
            },
            $("#frmSaveEmployee"),
            $scope,
            function () {
                  sparrow.redirect("#/spw_test/employees");
                
            });
        };

        $scope.onClose = function () {
            sparrow.redirect("#/spw_test/employees");
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
employeeInit();