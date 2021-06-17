const WAS_SET_MANUALLY_ATTRIBUTE = 'data-setmanual';

const hoursElement = document.getElementById('hours');
const hourlyRateElement = document.getElementById('hourly_rate');
const employeeContainerElement = document.getElementById('employees')
const expensesElement = document.getElementById('expenses');
const laborElement = document.getElementById('labor');
const suppliesElement = document.getElementById('supplies');
const miscElement = document.getElementById('misc');
const profitElement = document.getElementById('profit');
const profitMarginElement = document.getElementById('profit_margin');
const subtotalElement = document.getElementById('subtotal');
const taxElement = document.getElementById('tax');
const taxRateElement = document.getElementById('tax_rate');
const grandTotalElement = document.getElementById('grand-total');

function calculateHourlyRate() {
    let hourlyRate = 0;

    // sum the rate of all active employees
    for (const employeeElement of document.querySelectorAll('.active.employee')) {
        const rate = employeeElement.querySelector('[data-value]').getAttribute('data-value');

        hourlyRate += parseFloat(rate);
    }

    hourlyRateElement.value = asDecimal(hourlyRate);

    calculateLabor({ hourlyRate });
}


function calculateLabor({ hours, hourlyRate } = {}) {
    if (!hours) hours = parseFloat(hoursElement.value);
    if (!hourlyRate) hourlyRate = parseFloat(hourlyRateElement.value);

    let labor, laborValue;

    if (isNaN(hours) || isNaN(hourlyRate)) {
        labor = "NaN";

    } else {
        laborValue = hours * hourlyRate;
        labor = asDecimal(laborValue);
    }

    laborElement.value = labor;

    console.log({ hours, hourlyRate, laborValue, labor });

    calculateExpenses({ labor: laborValue });
}


function calculateExpenses({ labor, supplies, misc } = {}) {
    if (!labor) labor = parseFloat(laborElement.value);
    if (!supplies) supplies = parseFloat(suppliesElement.value);
    if (!misc) misc = parseFloat(miscElement.value);

    let expenses, expensesValue;

    if (isNaN(labor) || isNaN(supplies) || isNaN(misc)) {
        expenses = "NaN";

    } else {
        expensesValue = labor + supplies + misc;
        expenses = asDecimal(expensesValue);
    }

    expensesElement.innerText = expenses;

    // recalculate profit only if the profit margin was not manually set
    if (profitElement.hasAttribute(WAS_SET_MANUALLY_ATTRIBUTE)) {
        calculateSubtotal({ expenses: expensesValue });

    } else {
        calculateProfit({ expenses: expensesValue });
    }
}


function calculateProfit({ expenses, profitMargin } = {}) {
    if (!expenses) expenses = parseFloat(expensesElement.innerText);
    if (!profitMargin) profitMargin = parseFloat(profitMarginElement.value) / 100;

    let profit, profitValue;

    if (isNaN(expenses) || isNaN(profitMargin)) {
        profit = "NaN";

    } else {
        profitValue = profitMargin * expenses;
        profit = asDecimal(profitValue);
    }

    profitElement.value = profit;

    calculateSubtotal({ expenses, profit: profitValue });
}


function calculateSubtotal({ expenses, profit } = {}) {
    if (!expenses) expenses = parseFloat(expensesElement.innerText);
    if (!profit) profit = parseFloat(profitElement.value);

    let subtotal, subtotalValue;

    if (isNaN(expenses) || isNaN(profit)) {
        subtotal = "NaN";

    } else {
        subtotalValue = expenses + profit;
        subtotal = asDecimal(subtotalValue);

    }

    subtotalElement.innerText = subtotal;

    calculateTax({ subtotal: subtotalValue });
}


function calculateTax({ subtotal, taxRate } = {}) {
    if (!subtotal) subtotal = parseFloat(subtotalElement.innerText);
    if (!taxRate) taxRate = parseFloat(taxRateElement.value) / 100;

    let tax, taxValue;

    if (isNaN(subtotal) || isNaN(taxRate)) {
        tax = "NaN";

    } else {
        taxValue = subtotal * taxRate;
        tax = asDecimal(taxValue);
    }

    taxElement.innerText = tax;

    calculateGrandTotal({ subtotal, tax: taxValue });
}


function calculateGrandTotal({ subtotal, tax } = {}) {
    if (!subtotal) subtotal = parseFloat(subtotalElement.innerText);
    if (!tax) tax = parseFloat(taxElement.innerText);

    let grandTotal;

    if (isNaN(subtotal) || isNaN(tax)) {
        grandTotal = "NaN";

    } else {
        grandTotalValue = subtotal + tax;
        grandTotal = asDecimal(grandTotalValue);
    }

    grandTotalElement.innerText = grandTotal;
}


function asDecimal(str, places=2) {
    const val = parseFloat(str);
    const mod = 10 * places;

    return ((mod * val) / mod).toFixed(places);
}

hoursElement.addEventListener('input', calculateLabor);

hourlyRateElement.addEventListener('input', () => {
    document.querySelectorAll('.active.employee')
        .forEach(element => {
            element.classList.remove('active');
            element.classList.remove('bg-dark');
            element.classList.remove('text-white');
        });
    calculateLabor();
});

for (const employeeElement of document.querySelectorAll('.employee')) {
    employeeElement.addEventListener('click', calculateHourlyRate);
}

laborElement.addEventListener('input', () => {
    calculateExpenses();
    hourlyRateElement.value = "--";
});

suppliesElement.addEventListener('input', calculateExpenses);
miscElement.addEventListener('input', calculateExpenses);

profitElement.addEventListener('input', () => {
    calculateSubtotal();
    if (!profitElement.hasAttribute(WAS_SET_MANUALLY_ATTRIBUTE)) {
        profitElement.classList.add(WAS_SET_MANUALLY_ATTRIBUTE);
    }
    profitMarginElement.value = "--";
});

profitMarginElement.addEventListener('input', () => {
    profitElement.classList.remove(WAS_SET_MANUALLY_ATTRIBUTE);
    calculateProfit();
});

taxRateElement.addEventListener('input', calculateTax);

calculateHourlyRate();