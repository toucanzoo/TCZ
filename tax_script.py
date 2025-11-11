from textwrap import dedent


PERSONAL_ALLOWANCE = 12_570
PERSONAL_ALLOWANCE_TAPER_THRESHOLD = 100_000
BASIC_THRESHOLD = 50_270
ADDITIONAL_THRESHOLD = 125_140
BASIC_RATE = 0.20
HIGHER_RATE = 0.40
ADDITIONAL_RATE = 0.45

NI_LOWER = 12_570
NI_UPPER = 50_270
NI_MAIN_RATE = 0.12
NI_ADDITIONAL_RATE = 0.02


def get_personal_allowance(income: float) -> float:
    """Return the personal allowance after tapering for high earners."""
    if income <= PERSONAL_ALLOWANCE_TAPER_THRESHOLD:
        return PERSONAL_ALLOWANCE
    reduction = (income - PERSONAL_ALLOWANCE_TAPER_THRESHOLD) / 2
    allowance = max(0.0, PERSONAL_ALLOWANCE - reduction)
    return allowance


def calculate_income_tax(income: float) -> float:
    allowance = get_personal_allowance(income)
    taxable_income = max(0.0, income - allowance)

    if taxable_income == 0:
        return 0.0

    tax = 0.0

    basic_band = min(taxable_income, BASIC_THRESHOLD - allowance)
    tax += basic_band * BASIC_RATE

    if taxable_income > basic_band:
        higher_band = min(
            taxable_income - basic_band,
            ADDITIONAL_THRESHOLD - BASIC_THRESHOLD,
        )
        tax += higher_band * HIGHER_RATE
    else:
        return tax

    remaining = taxable_income - basic_band - higher_band
    if remaining > 0:
        tax += remaining * ADDITIONAL_RATE

    return tax


def calculate_national_insurance(income: float) -> float:
    if income <= NI_LOWER:
        return 0.0

    ni_taxable = income - NI_LOWER
    ni = 0.0

    main_band = min(ni_taxable, NI_UPPER - NI_LOWER)
    ni += main_band * NI_MAIN_RATE

    additional_band = ni_taxable - main_band
    if additional_band > 0:
        ni += additional_band * NI_ADDITIONAL_RATE

    return ni


def format_currency(value: float) -> str:
    return f"£{value:,.2f}"


def print_tax_allowances() -> None:
    summary = dedent(
        f"""
        UK Income Tax Bands (2024/25):
          • Personal Allowance: {format_currency(PERSONAL_ALLOWANCE)} (reduced £1 for every £2 above {format_currency(PERSONAL_ALLOWANCE_TAPER_THRESHOLD)} until it reaches £0 at {format_currency(ADDITIONAL_THRESHOLD)})
          • Basic Rate (20%): taxable income up to {format_currency(BASIC_THRESHOLD)}
          • Higher Rate (40%): portion between {format_currency(BASIC_THRESHOLD)} and {format_currency(ADDITIONAL_THRESHOLD)}
          • Additional Rate (45%): portion above {format_currency(ADDITIONAL_THRESHOLD)}

        National Insurance (Class 1 employee rates):
          • 12% on earnings between {format_currency(NI_LOWER)} and {format_currency(NI_UPPER)}
          • 2% on earnings above {format_currency(NI_UPPER)}
        """
    ).strip()

    print(summary)


def show_summary_for_income(income: float) -> None:
    allowance = get_personal_allowance(income)
    tax = calculate_income_tax(income)
    ni = calculate_national_insurance(income)

    print("\nExample salary analysis:")
    print(f"  Gross salary: {format_currency(income)}")
    print(f"  Personal allowance applied: {format_currency(allowance)}")
    print(f"  Income tax due: {format_currency(tax)}")
    print(f"  National Insurance due: {format_currency(ni)}")
    print(f"  Total deductions: {format_currency(tax + ni)}")
    print(f"  Net pay: {format_currency(income - tax - ni)}")


if __name__ == "__main__":
    print_tax_allowances()
    show_summary_for_income(145_000)
