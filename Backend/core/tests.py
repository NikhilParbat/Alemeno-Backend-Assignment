from datetime import date
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer, Loan


class CustomerLoanAPITests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            monthly_income=50000,
            approved_limit=1800000,
            phone_number=1234567890
        )
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=100000,
            tenure=12,
            interest_rate=10,
            monthly_installment=8791,
            emis_paid_on_time=5,
            start_date=date.today(), 
            end_date = (timezone.now() + timezone.timedelta(days=12 * 30)).date(),
        )

    # ------------------ Register Customer ------------------
    def test_register_customer_success(self):
        url = reverse("register-customer")
        data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "age": 28,
            "monthly_income": 60000,
            "phone_number": 9876543210
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_register_customer_missing_field(self):
        url = reverse("register-customer")
        data = {
            "first_name": "Bob",
            "age": 40,
            "monthly_income": 40000
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ------------------ Check Eligibility ------------------
    def test_check_eligibility_success(self):
        url = reverse("check-eligibility")
        data = {
            "customer_id": self.customer.id,
            "loan_amount": 50000,
            "interest_rate": 12,
            "tenure": 12
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("approval", response.data)

    def test_check_eligibility_invalid_customer(self):
        url = reverse("check-eligibility")
        data = {
            "customer_id": 9999,
            "loan_amount": 50000,
            "interest_rate": 12,
            "tenure": 12
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ------------------ Create Loan ------------------
    def test_create_loan_success(self):
        url = reverse("create-loan")
        data = {
            "customer_id": self.customer.id,
            "loan_amount": 75000,
            "interest_rate": 12,
            "tenure": 10
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["loan_approved"])

    def test_create_loan_invalid_customer(self):
        url = reverse("create-loan")
        data = {
            "customer_id": 8888,
            "loan_amount": 50000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_loan_rejected_due_to_income(self):
        low_income_customer = Customer.objects.create(
            first_name="Poor",
            last_name="Guy",
            age=40,
            monthly_income=1000,
            approved_limit=10000,
            phone_number=1112223333
        )
        url = reverse("create-loan")
        data = {
            "customer_id": low_income_customer.id,
            "loan_amount": 500000,
            "interest_rate": 8,
            "tenure": 12
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(response.data["loan_approved"])

    # ------------------ View Single Loan ------------------
    def test_view_single_loan_success(self):
        url = reverse("view-loan", kwargs={"id": self.loan.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.loan.id)

    def test_view_single_loan_not_found(self):
        url = reverse("view-loan", kwargs={"id": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ------------------ View Customer Loans ------------------
    def test_view_customer_loans_success(self):
        url = reverse("view-loans", kwargs={"customer_id": self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_view_customer_loans_not_found(self):
        url = reverse("view-loans", kwargs={"customer_id": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
