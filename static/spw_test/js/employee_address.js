function employeeAddressInit(data) {
  sparrow.registerCtrl(
    "employeeAddressCtrl",
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
        pageTitle: "Employee Address",
        topActionbar: {},
      };

        setAutoLookup("id_employee", '/spw_test/lookups/employee/', '')

        var stateData = [
            {id: "Gujarat", name: "Gujarat"},
            {id: "Maharashtra", name: "Maharashtra"},
            {id: "Rajasthan", name: "Rajasthan"},
            {id: "Karnataka", name: "Karnataka"},
            {id: "Tamil Nadu", name: "Tamil Nadu"},
            {id: "Uttar Pradesh", name: "Uttar Pradesh"},
            {id: "West Bengal", name: "West Bengal"},
            {id: "Punjab", name: "Punjab"},
            {id: "Haryana", name: "Haryana"},
            {id: "Kerala", name: "Kerala"}
        ];
        var districtData = [
            {id: "Ahmedabad", name: "Ahmedabad"},
            {id: "Mumbai", name: "Mumbai"},
            {id: "Jaipur", name: "Jaipur"},
            {id: "Bengaluru", name: "Bengaluru"},
            {id: "Chennai", name: "Chennai"},
            {id: "Lucknow", name: "Lucknow"},
            {id: "Kolkata", name: "Kolkata"},
            {id: "Ludhiana", name: "Ludhiana"},
            {id: "Gurgaon", name: "Gurgaon"},
            {id: "Thiruvananthapuram", name: "Thiruvananthapuram"}
        ];
        var countryData = [
            {id: "India", name: "India"},
            {id: "United States", name: "United States"},
            {id: "United Kingdom", name: "United Kingdom"},
            {id: "Canada", name: "Canada"},
            {id: "Australia", name: "Australia"},
            {id: "Germany", name: "Germany"},
            {id: "France", name: "France"},
            {id: "Japan", name: "Japan"},
            {id: "China", name: "China"},
            {id: "Brazil", name: "Brazil"}
        ];

        setAutoLookup("id_state", stateData, '');
        setAutoLookup("id_district", districtData, '');
        setAutoLookup("id_country", countryData, '');


        $scope.saveEmployeeAddress = function () {
            console.log("here");
            
            var employee = $("#hid_employee").val();
                if (!employee) {
                    console.log("error")
                    sparrow.showMessage("appMsg", sparrow.MsgType.Error, "Employee should be selected", 5);
                    return;
                }
            var district = $("#hid_district").val();
                if (!district) {
                    sparrow.showMessage("appMsg", sparrow.MsgType.Error, "District should be selected", 5);
                    return;
                }
            var state = $("#hid_state").val();
                if (!state) {
                    sparrow.showMessage("appMsg", sparrow.MsgType.Error, "State should be selected", 5);
                    return;
                }
            var country = $("#hid_country").val();
                if (!country) {
                    sparrow.showMessage("appMsg", sparrow.MsgType.Error, "Country should be selected", 5);
                    return;
                }

            sparrow.postForm(
                {
                    address_id: $routeParams.id,
                },
                $("#frmSaveEmployeeAddress"),
                $scope,
                function () {
                     sparrow.redirect("#/spw_test/employees_address");
                }
            );
        };

        $scope.onClose = function () {
            sparrow.redirect("#/spw_test/employees_address");
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