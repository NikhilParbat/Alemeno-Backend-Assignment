from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Customer, Loan
from .serializers import (
    RegisterSerializer,
    CustomSerializer,
    ProcessLoanSerializer,
    LoanDetailSerializer,
    LoanListSerializer,
)
from .services import check_loan_eligibility, process_new_loan


@api_view(["POST"])
def register_customer(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        return Response(CustomSerializer(customer).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def check_eligibility(request):
    customer_id = request.data.get("customer_id")
    loan_amount = request.data.get("loan_amount")
    interest_rate = request.data.get("interest_rate")
    tenure = request.data.get("tenure")

    customer = get_object_or_404(Customer, pk=customer_id)

    result = check_loan_eligibility(
        customer=customer,
        loan_amount=float(loan_amount),
        interest_rate=float(interest_rate),
        tenure=int(tenure),
    )
    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
def process_loan(request):
    serializer = ProcessLoanSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    customer = get_object_or_404(Customer, pk=data["customer_id"])

    result = process_new_loan(
        customer,
        data["loan_amount"],
        data["interest_rate"],
        data["tenure"],
    )

    if not result["loan_approved"]:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(result, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def loan_detail(request, id):
    loan = get_object_or_404(Loan, id=id)
    serializer = LoanDetailSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def view_customer_loans(request, customer_id):
    get_object_or_404(Customer, id=customer_id)
    loans = Loan.objects.filter(customer_id=customer_id)
    serializer = LoanListSerializer(loans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
