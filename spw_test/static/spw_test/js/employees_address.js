function employeesAddressInit() {
  sparrow.registerCtrl(
    "employeesAddressCtrl",
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
        pageTitle: "Employee Address",
        topActionbar: {
            add: {
                url: baseUrl+'spw_test/employee_address/',
            },
            edit: {
                url: baseUrl+'spw_test/employee_address/',
            },
            delete: {
                url: '/spw_test/employee_address_delete/',
            }
        },
        listing: [
          {
            index: 1,
            url: "/spw_test/employee_address_search/",
            crud: true,
            postData: {
              employeeId: employeeId
            }, 
            search: {
                params: [
                    { key: "employee",name:"Employee" },
                    { key: "address", name: "Address" },
                    { key: "district", name: "District" },
                    { key: "state", name: "State" },
                    { key: "country", name: "Country" },
                    { key: "pin_code", name: "Pin Code"}
                ],
            },
            columns: [
              {
                name: "employee",
                title: "Employee",
                renderWith: function(data, type, full, meta) {
                    return `<a href= "${ baseUrl }spw_test/employee_address/${full.id}">${data}</a>`
                }
              },
              {
                name: "address",
                title: "Address",
                renderWith: function(data, type, full, meta) {
                    return `<a href= "${ baseUrl }spw_test/employee_address/${full.id}">${data}</a>`
                }
              },
              {
                name: "district",
                title: "District",
              },
              {
                name: "state",
                title: "State",
              },
              {
                name: "country",
                title: "Country",
              },
              {
                name: "pin_code",
                title: "Pin code",
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