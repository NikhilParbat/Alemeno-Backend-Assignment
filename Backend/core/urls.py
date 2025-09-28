from django.urls import path
from .views import (
    register_customer,
    check_eligibility,
    process_loan,
    loan_detail,
    view_customer_loans,
)

urlpatterns = [
    path("register/", register_customer, name="register-customer"),
    path("check-eligibility/", check_eligibility, name="check-eligibility"),
    path("create-loan/", process_loan, name="create-loan"),
    path("view-loan/<int:id>/", loan_detail, name="view-loan"),
    path("view-loans/<int:customer_id>/", view_customer_loans, name="view-loans"),
]
