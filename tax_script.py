PERSONAL_ALLOWANCE = 12570
BASIC_THRESHOLD = 50270
HIGHER_THRESHOLD = 125140
BASIC_RATE = 0.20
HIGHER_RATE = 0.40
ADDITIONAL_RATE = 0.45

NI_LOWER = 12570
NI_UPPER = 50270
NI_MAIN_RATE = 0.12
NI_ADDITIONAL_RATE = 0.02


def calculate_income_tax(income):
    if income <= PERSONAL_ALLOWANCE:
        return 0
    taxable = income - PERSONAL_ALLOWANCE
    tax = 0
    if income <= BASIC_THRESHOLD:
        tax += taxable * BASIC_RATE
    elif income <= HIGHER_THRESHOLD:
        tax += (BASIC_THRESHOLD - PERSONAL_ALLOWANCE) * BASIC_RATE
        tax += (income - BASIC_THRESHOLD) * HIGHER_RATE
    else:
        tax += (BASIC_THRESHOLD - PERSONAL_ALLOWANCE) * BASIC_RATE
        tax += (HIGHER_THRESHOLD - BASIC_THRESHOLD) * HIGHER_RATE
        tax += (income - HIGHER_THRESHOLD) * ADDITIONAL_RATE
    return tax


def calculate_national_insurance(income):
    if income <= NI_LOWER:
        return 0
    ni_taxable = income - NI_LOWER
    ni = 0
    if income <= NI_UPPER:
        ni += ni_taxable * NI_MAIN_RATE
    else:
        ni += (NI_UPPER - NI_LOWER) * NI_MAIN_RATE
        ni += (income - NI_UPPER) * NI_ADDITIONAL_RATE
    return ni


if __name__ == '__main__':
    income = 120000
    tax = calculate_income_tax(income)
    ni = calculate_national_insurance(income)
    print(f"Estimated income tax: £{tax:,.2f}")
    print(f"Estimated NI: £{ni:,.2f}")
    print(f"Estimated total deductions: £{tax + ni:,.2f}")
