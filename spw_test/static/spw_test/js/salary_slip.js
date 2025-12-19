function salarySlipInit() {
    sparrow.registerCtrl('salarySlipCtrl', function (
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
            pageTitle: 'Salary Slip',
            topActionbar: {},
        };

        function calculateOnChange() {

            const basic = +$("#basic").val() || 0;
            const hra = +$("#hra").val() || 0;
            const special = +$("#special").val() || 0;
            const otherAllowance = +$("#otherAllowance").val() || 0;
            const conveyance = +$("#conveyance").val() || 0;
            const medical = +$("#medical").val() || 0;

            const pf = +$("#pf").val() || 0;
            const otherDeduction = +$("#otherDeduction").val() || 0;
            const tds = +$("#tds").val() || 0;
            const professionalTax = +$("#professionalTax").val() || 0;

            const lwp = +$("#lwp").val() || 0;
            const totalDays = +$("#totalDays").text() || 0;

            const gross =
                basic + hra + special + otherAllowance + conveyance + medical;

            const lwpDeduction =
                totalDays > 0 ? ((gross / totalDays) * lwp) : 0;

            const deductions =
                pf + lwpDeduction + otherDeduction + tds + professionalTax;

            const net = gross - deductions;

            $("#grossEarnings").text(gross.toFixed(2));
            $("#lwp_deduction").text(lwpDeduction.toFixed(2));
            $("#lwpDeduction").val(lwpDeduction.toFixed(2));
            $("#totalDeductions").text(deductions.toFixed(2));
            $("#netSalary").text("₹" + net.toFixed(2));

        }
        
        $("#conveyance, #medical, #tds, #lwp").on("input", calculateOnChange);
        
        $('#payPeriod').on('change', function () {           
            const month = $(this).val();

            if (!month) {
                sparrow.showMessage(
                    "appMsg",
                    sparrow.MsgType.Error,
                    "Please select month",
                    5
                );
                return;
            }

            sparrow.postForm(
                { month: month },
                $("#frmDateUpdate"),
                $scope,
                function (data) {

                    if (data.total_days !== undefined) {
                        $('#totalDays').text(data.total_days);
                    }

                    if (data.leaves_taken !== undefined) {
                        $('#leavesTaken').text(data.leaves_taken);
                    }

                    if (data.lwp !== undefined) {
                        $('#lwp').val(data.lwp);
                        $('#lwpf').text(data.lwp);
                    }

                    calculateOnChange(); 
                }
            );
        });

        $scope.onDownload = function () {
            const payload = {
                emp_id: $("#employee_id").val(),
                selected_month: $("#payPeriod").val(),
                month: $("#payPeriod").val(),
                emp_designation: $("#emp_designation").text(),
                emp_name: $("#emp_name").text(),
                total_days: $("#totalDays").text(),
                leaves_taken: $("#leavesTaken").text(),
                lwp: $("#lwpf").text(),

                basic: $("#basic_salary").text(),
                hra: $("#hra_salary").text(),
                special: $("#special_allowance").text(),
                other_allowance: $("#other_allowance").text(),
                conveyance: $("#conveyance").val(),
                medical: $("#medical").val(),

                pf: $("#pf_salary").text(),
                lwp_deduction: $("#lwp_deduction").text(),
                other_deduction: $("#other_deduction").text(),
                tds: $("#tds").val(),
                professional_tax: $("#professional_tax").text(),

                gross_earnings: $("#grossEarnings").text(),
                total_deductions: $("#totalDeductions").text(),
                net_salary: $("#netSalary").text().replace("₹", "")
            };

            $("#pdfPayload").val(JSON.stringify(payload));
            $("#pdfDownloadForm").submit();
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
    });
}

salarySlipInit();
