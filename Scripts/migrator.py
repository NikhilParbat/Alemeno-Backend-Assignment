import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from django.conf import settings

# Database connection details (should match Django settings)
DB_CONFIG = {
    "dbname": "credit_approval",
    "user": "root",
    "password": "1111",
    "host": "localhost",
    "port": "5433"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def ingest_customers(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    df = pd.read_excel(file_path)
    records = df.to_dict(orient="records")

    insert_query = """
    INSERT INTO core_customer
    (customer_id, first_name, last_name, age, phone_number, monthly_income, approved_limit)
    VALUES %s
    ON CONFLICT (customer_id) DO NOTHING;
    """

    values = [
        (
            r["Customer ID"],
            r["First Name"],
            r["Last Name"],
            r["Age"],
            r["Phone Number"],
            r["Monthly Salary"],
            r["Approved Limit"],
        )
        for r in records
    ]
    return insert_query, values


def ingest_loans(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    df = pd.read_excel(file_path)
    records = df.to_dict(orient="records")

    insert_query = """
    INSERT INTO core_loan
    (loan_id, customer_id, loan_amount, tenure, interest_rate,
     monthly_installment, emis_paid_on_time, start_date, end_date)
    VALUES %s
    ON CONFLICT (loan_id) DO NOTHING;
    """

    values = [
        (
            r["Loan ID"],
            r["Customer ID"],
            r["Loan Amount"],
            r["Tenure"],
            r["Interest Rate"],
            r["Monthly payment"],
            r["EMIs paid on Time"],
            r["Date of Approval"],
            r["End Date"]
        )
        for r in records
    ]
    return insert_query, values


def run_ingestion():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Ingest customers
    query, values = ingest_customers("../customer_data.xlsx")
    execute_values(cur, query, values)

    # Ingest loans
    query, values = ingest_loans("../loan_data.xlsx")
    execute_values(cur, query, values)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Data ingestion complete!")


if __name__ == "__main__":
    run_ingestion()
