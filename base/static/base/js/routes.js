sparrow.config([
  "$routeProvider",
  "$controllerProvider",
  function ($routeProvider, $controllerProvider) {
    sparrow.registerCtrl = $controllerProvider.register;

    function loadScript(path) {
      var result = $.Deferred(),
        script = document.createElement("script");
      script.async = "async";
      script.type = "text/javascript";
      script.src = sparrow.getStaticUrl() + path;
      script.onload = script.onreadystatechange = function (_, isAbort) {
        if (!script.readyState || /loaded|complete/.test(script.readyState)) {
          if (isAbort) result.reject();
          else result.resolve();
        }
      };
      script.onerror = function () {
        result.reject();
      };
      var scriptContainer =
        $("#viewContainer").length != 0
          ? document.getElementById("viewContainer")
          : document.querySelector("body");
      scriptContainer.appendChild(script);
      return result.promise();
    }

    function loader(arrayName) {
      return {
        load: function ($q) {
          var deferred = $q.defer(),
            map = arrayName.map(function (name) {
              return loadScript(name);
            });
          $q.all(map).then(function (r) {
            deferred.resolve();
          });
          return deferred.promise;
        },
      };
    }

    $routeProvider.when("/testpage", {
      templateUrl: "/spw_test/testpage/",
      controller: "testCtrl",

    })

      .when('/search', {
        templateUrl: '/base/search/',
        controller: 'appSearchCtrl',
        resolve: loader(['base/js/app_search.js']),

      })
      .when('/hello', {
        templateUrl: '/spw_test/hello/',
      })
      // .when('/spw_test/employees', {
      //   templateUrl: '/spw_test/employees/',
      //   controller: 'employeesCtrl',
      //   resolve: loader(['spw_test/js/employees.js']),
      // })

      .when('/spw_test/employees', {
        templateUrl: '/spw_test/employees/',
        controller: 'employeesCtrl',
        resolve: loader(['spw_test/js/employees.js']),
      })
      .when('/spw_test/employee/:id/', {
        templateUrl: function (urlattr) {
          return '/spw_test/employee/' + urlattr.id + '/';
        },
        controller: 'employeeCtrl',
        resolve: loader(['spw_test/js/employee.js?v=0.1']),
      })

      .when('/spw_test/employees_address', {
        templateUrl: '/spw_test/employees_address/',
        controller: 'employeesAddressCtrl',
        resolve: loader(['spw_test/js/employees_address.js']),
      })

      .when('/spw_test/employees_address/:id/', {
        templateUrl: function (urlattr) {
          return '/spw_test/employees_address/' + urlattr.id + '/';
        },
        controller: 'employeesAddressCtrl',
        resolve: loader(['spw_test/js/employees_address.js?v=0.1']),
      })

      .when('/spw_test/employee_address/:id/', {
        templateUrl: function (urlattr) {
          return '/spw_test/employee_address/' + urlattr.id + '/';
        },
        controller: 'employeeAddressCtrl',
        resolve: loader(['spw_test/js/employee_address.js?v=0.1']),
      })


      .when('/spw_test/employees_leave', {
        templateUrl: '/spw_test/employees_leave/',
        controller: 'employeesLeaveCtrl',
        resolve: loader(['spw_test/js/employees_leave.js']),
      })

      .when('/spw_test/employees_leave/:id/', {
        templateUrl: function (urlattr) {
          return '/spw_test/employees_leave/' + urlattr.id + '/';
        },
        controller: 'employeesLeaveCtrl',
        resolve: loader(['spw_test/js/employees_leave.js?v=0.1']),
      })

      .when('/spw_test/employee_leave/:id/', {
        templateUrl: function (urlattr) {
          return '/spw_test/employee_leave/' + urlattr.id + '/';
        },
        controller: 'employeeLeaveCtrl',
        resolve: loader(['spw_test/js/employee_leave.js?v=0.2']),
      })

      .when('/spw_test/employees_leaves_master', {
        templateUrl: '/spw_test/employees_leaves_master/',
        controller: 'employeesLeavesMasterCtrl',
        resolve: loader(['spw_test/js/employees_leaves_master.js']),
      })

      .when('/spw_test/salary_slip/:id/', {
        templateUrl: function (urlattr) {
          return '/spw_test/salary_slip/' + urlattr.id + '/';
        },
        controller: 'salarySlipCtrl',
        resolve: loader(['spw_test/js/salary_slip.js']),
      })
  },
]);
