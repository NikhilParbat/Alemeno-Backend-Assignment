# 🏦 Credit Approval System

A Django + PostgreSQL application to manage **loan eligibility, approvals, and tracking**.  
It includes APIs to register customers, check loan eligibility, create new loans, and view loan details — all fully containerized with Docker.

---

## 🚀 Features

- 👤 **Customer Management** – Register new customers with personal and financial details.  
- 📊 **Loan Eligibility Check** – Smart scoring algorithm based on:
  - Income
  - Past repayments
  - Existing loans
  - Credit utilization  
- 💰 **Loan Processing** – Approve/reject new loans automatically with corrected interest rates.  
- 🔎 **Loan Tracking**:
  - View details of a single loan
  - List all active loans for a customer  
- 🐳 **Dockerized Setup** – Runs with Docker Compose (Postgres + Django).  
- ⚡ **Database Seeder** – Initial dataset pushed via `Scripts/migrator.py`.

---

## 🏗️ Tech Stack

- **Backend:** Django REST Framework  
- **Database:** PostgreSQL (Dockerized)  
- **Containerization:** Docker & Docker Compose  
- **ORM:** Django ORM  
- **Testing:** Django Unit Tests (positive & negative cases)  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/NikhilParbat/Alemeno-Backend-Assignment
cd Alemeno-Backend-Assignment
```
In the root folder:

# Database
```
POSTGRES_USER=root
POSTGRES_PASSWORD=1111
POSTGRES_DB=credit_approval
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
3️⃣ Run with Docker Compose
```
docker-compose up --build
```

This will:

Start a Postgres 16 database (db service).

Run Django migrations.

Seed initial data via 
```
Scripts/migrator.py.
```
Launch the server at http://localhost:8000
```
python manage.py runserver
```
