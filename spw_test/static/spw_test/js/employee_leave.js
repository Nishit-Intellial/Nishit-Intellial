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
        topActionbar: {}
      };

      setAutoLookup("id_employee", "/spw_test/lookups/employee/", "");
      setAutoLookup("id_leavetype", "/spw_test/lookups/leavetype/", "");

      function updateLeaveDurationTable() {
        var startDate = $("#id_leave_start_date").val();
        var endDate = $("#id_leave_end_date").val();

        if (!(startDate && endDate)) {
          $("#leaveDurationTableContainer").hide();
          return;
        }

        var start = new Date(startDate);
        var end = new Date(endDate);

        var tableBody = $("#durationTable tbody");
        tableBody.empty();

        var currentDate = new Date(start);

        while (currentDate <= end) {
          var dateStr = currentDate.toISOString().split("T")[0];

          var row = $("<tr>");
          row.append($("<td>").text(dateStr));

          var inputId = "duration_" + dateStr;
          var input = $('<input type="text" class="form-control" name="id_'+dateStr+'" id="' + inputId + '">');

          row.append($("<td>").append(input));
          tableBody.append(row);

          setAutoLookup(inputId, "/spw_test/lookups/leaveduration/", "").setSelection([{ id: 3, name: "1" }]);;

          currentDate.setDate(currentDate.getDate() + 1);
        }

        $("#leaveDurationTableContainer").show();
      }

      function collectLeaveDurations() {
        var leaveData = {};

        $("#durationTable tbody tr").each(function () {
          var date = $(this).find("td:first").text();
          var inputId = $(this).find("input").attr("id");
          leaveData[date] = $("#hid_" + inputId).val() || "";
        });

        var hiddenInput = $("#leaveDataInput");
        if (!hiddenInput.length) {
          hiddenInput = $("<input>", {
            type: "hidden",
            id: "leaveDataInput",
            name: "leave_data"
          });
          $("#frmSaveEmployeeLeave").append(hiddenInput);
        }

        hiddenInput.val(JSON.stringify(leaveData));
      }

      $("#id_leave_start_date").on("change", function () {
        var start = $(this).val();
        var endInput = $("#id_leave_end_date");
        endInput.attr("min", start);
        if (endInput.val() && endInput.val() < start) {
          endInput.val(start);
        }
        updateLeaveDurationTable();
      });

      $("#id_leave_end_date").on("change", function () {
        updateLeaveDurationTable();
      });

      $scope.saveEmployeeLeave = function () {
        collectLeaveDurations();

        var employee = $("#hid_employee").val();
        if (!employee) {
          sparrow.showMessage("appMsg", sparrow.MsgType.Error, "Employee should be selected", 5);
          return;
        }

        var leave_type = $("#hid_leavetype").val();
        if (!leave_type) {
          sparrow.showMessage("appMsg", sparrow.MsgType.Error, "Leave Type should be selected", 5);
          return;
        }

        sparrow.postForm(
          { employeeleave_id: $routeParams.id },
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
