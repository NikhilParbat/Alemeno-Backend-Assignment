from .models import Loan
from .utils import calculate_emi
from datetime import date
from django.utils import timezone

def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    loans = Loan.objects.filter(customer=customer)
    score = 100

    if sum(l.loan_amount for l in loans if l.end_date >= date.today()) > customer.approved_limit:
        score = 0

    on_time = sum(1 for l in loans if l.emis_paid_on_time >= (l.tenure * 0.9))
    score += on_time * 5
    score -= len(loans) * 2

    current_year_loans = sum(1 for l in loans if l.start_date.year == date.today().year)
    score -= current_year_loans * 3

    approved_volume = sum(l.loan_amount for l in loans)
    score -= approved_volume / 1000000

    score = max(0, min(100, score))

    if score > 50:
        corrected_rate = interest_rate
    elif score > 30:
        corrected_rate = max(12, interest_rate)
    elif score > 10:
        corrected_rate = max(16, interest_rate)
    else:
        return {
            "customer_id": customer.id,
            "approval": False,
            "interest_rate": interest_rate,
            "corrected_interest_rate": None,
            "tenure": tenure,
            "monthly_installment": None,
        }

    emis = sum(l.monthly_installment for l in loans if l.end_date >= date.today())
    if emis + calculate_emi(loan_amount, corrected_rate, tenure) > 0.5 * customer.monthly_income:
        return {
            "customer_id": customer.id,
            "approval": False,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_rate,
            "tenure": tenure,
            "monthly_installment": None,
        }

    return {
        "customer_id": customer.id,
        "approval": True,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_rate,
        "tenure": tenure,
        "monthly_installment": calculate_emi(loan_amount, corrected_rate, tenure),
    }


def process_new_loan(customer, loan_amount, interest_rate, tenure):
    eligibility = check_loan_eligibility(customer, loan_amount, interest_rate, tenure)

    if not eligibility["approval"]:
        return {
            "loan_id": None,
            "customer_id": customer.id,
            "loan_approved": False,
            "message": "Loan not approved",
            "monthly_installment": None
        }

    emi = eligibility["monthly_installment"]

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        tenure=tenure,
        interest_rate=eligibility["corrected_interest_rate"],
        monthly_installment=emi,
        emis_paid_on_time=0,
        start_date=timezone.now().date(),
        end_date=(timezone.now() + timezone.timedelta(days=tenure * 30)).date()
    )

    return {
        "loan_id": loan.id,
        "customer_id": customer.id,
        "loan_approved": True,
        "message": "Loan approved",
        "monthly_installment": emi
    }