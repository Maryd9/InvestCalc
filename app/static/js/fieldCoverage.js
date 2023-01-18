document.addEventListener("DOMContentLoaded", () => {
    function cleanFields(param) {
        indexes.addEventListener('change', function () {
            console.log(this.value);
            if (this.value === "NPV" , this.value === "PI", this.value === "DPP" , this.value === "IRR" , this.value === "MIRR") {
                param--;
                while (param > -1) {
                    document.getElementById('year' + param).value = '';
                    param--;
                }
                document.getElementById('initialInvestment').value = '';
                document.getElementById('cashflows').value = '';
                document.getElementById('discountRate').value = '';
            }
        });
    }

    function cleanFieldsCf() {
        for (let i = 2; i < 21; i++) {
            document.getElementById('year' + i).hidden = true;
        }
    }

    function addFieldsCf() {
        cashflows.addEventListener('change', function () {
            cleanFieldsCf();
            for (let i = 0; i <= this.value; i++) {
                document.getElementById('year' + i).hidden = false;
            }
        });
    }

    cleanFieldsCf();
    var years = document.getElementById('cashflows').value;
    cleanFields(years);
    addFieldsCf();

});