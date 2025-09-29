import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from django.conf import settings

# Database connection details (should match Django settings)
import os
import psycopg2
from dotenv import load_dotenv

# Load env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "credit_approval"),
    "user": os.getenv("POSTGRES_USER", "root"),
    "password": os.getenv("POSTGRES_PASSWORD", "1111"),
    "host": os.getenv("POSTGRES_HOST", "db"),  # use Docker service name
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

def run_ingestion():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # your ingestion logic
    # cur.execute(...)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    run_ingestion()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def ingest_customers(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    df = pd.read_excel(file_path)
    records = df.to_dict(orient="records")

    insert_query = """
    INSERT INTO core_customer
    (id, first_name, last_name, age, phone_number, monthly_income, approved_limit)
    VALUES %s
    ON CONFLICT (id) DO NOTHING;
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
    (id, customer_id, loan_amount, tenure, interest_rate,
     monthly_installment, emis_paid_on_time, start_date, end_date)
    VALUES %s
    ON CONFLICT (id) DO NOTHING;
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
