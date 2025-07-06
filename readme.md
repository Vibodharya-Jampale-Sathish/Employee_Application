# 🧾 Employee Management Application

This is a full-stack **Employee Management Web Application** built using **Python (Flask)** for the backend and **PostgreSQL** for data storage. It allows companies to register, log in, and manage their employees effectively.

---

## 📦 Features

- 🏢 Company Registration and Login
- 👤 Add, Edit, and View Employee Records
- 🔒 Secure authentication using session management
- 🗃️ PostgreSQL-based relational database with proper foreign key constraints
- 🧮 Form validation and error handling
- 📋 Clean and simple UI (HTML + CSS Bootstrap)

---

## ⚙️ Technologies Used

- Backend: Python (Flask)
- Frontend: HTML, CSS (Bootstrap)
- Database: PostgreSQL
- Templating: Jinja2

---

## 💾 Database
Run the database.sql file to create the required database for this project, or use pgAdmin to create the database using the structure defined in the SQL file.

---
## 🏗️ Application Architecture (3-Table Design)


```mermaid
flowchart TD
    %% User Actions
    A1[Register Page] --> R1[Register Route]
    A2[Login Page] --> R2[Login Route]
    A3[Dashboard Access] --> R3[Dashboard Route]
    A4[Add Department Form] --> R4[Department Route]
    A5[Add Employee Form] --> R5[Employee Route]
    A6[View Records Page] --> R6[View Route]

    %% Flask Routes to DB
    R1 --> DB1[Company_Login_Details]
    R2 --> DB1
    R3 --> DB1
    R4 --> DB2[Departments]
    R5 --> DB3[Employee_Details]
    R6 --> DB3

    %% Relationships
    DB2 -->|FK: Company_ID| DB1
    DB3 -->|FK: Company_ID| DB1
    DB3 -->|FK: Department_ID| DB2
```
---
## 🏗️ Project Structure


```bash
employee_application/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (DB credentials, secret key)
├── README.md                       # Project documentation
├── ARCHITECTURE.md                 # Architecture and Mermaid diagrams
│
├── /templates/                     # HTML templates
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── employee.html
│   ├── department.html
│   └── view.html
│
├── /static/                        # Static assets (optional: CSS, JS, images)
│   ├── styles.css
│   └── logo.png
│
├── /sql/                           # SQL setup scripts
│   └── schema.sql                  # CREATE TABLE statements for all 3 tables

```
## 🏗️ Env Structure

---

```env
DATABASE_URL= Use_your_External_URL
SECRET_KEY= Secret_Key_For_Flash

```
