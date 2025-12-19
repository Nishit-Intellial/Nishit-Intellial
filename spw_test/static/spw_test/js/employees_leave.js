function employeesAddressInit() {
  sparrow.registerCtrl(
    "employeesLeaveCtrl",
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
        pageTitle: "Employee Leaves",
        listing: [
          {
            index: 1,
            url: "/spw_test/employee_leave_search/",
            // crud: true,
            postData: {
              employeeId: employeeId
            }, 
            search: {
                params: [
                    { key: "employee",name:"Employee" },
                    { key: "leave_type",name:"Leave Type" },
                    { key: "leave_taken",name:"Leave Taken" },
                    { key: "allocated",name:"Allocated" },
                    { key: "balance",name:"Balance" },
                ],
            },
            columns: [
              {
                name: "employee",
                title: "Employee",
              },
              {
                name:"leave_type",
                title:"Leave Type"
              },
              {
                name:"taken_leave",
                title:"Taken Leave"
              },
              {
                name:"allocated",
                title:"Allocated"
              },
              {
                name:"balance",
                title:"Balance"
              },
              
            ],
          },
        ],
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

employeesAddressInit();