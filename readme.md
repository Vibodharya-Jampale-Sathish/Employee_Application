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
Thanks again, and you're absolutely right — GitHub's Mermaid parser is very strict. The issue here is using [/route] notation. GitHub does not support slashes (/) or square brackets around node labels unless they follow Mermaid’s syntax rules precisely.

✅ Fixed, GitHub-Compatible Mermaid Diagram
Here is a fully valid Mermaid diagram that will render without errors on GitHub:

mermaid
Copy
Edit
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
