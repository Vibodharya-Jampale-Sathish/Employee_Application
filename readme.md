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
    subgraph User
        A[User Browser]
        A1[Login/Register Page]
        A2[Add Employee / Blog]
        A3[View Records]
    end

    subgraph Flask_App
        B[Flask Routes]
        B1[/register]
        B2[/login]
        B3[/add]
        B4[/view]
        B5[/logout]
    end

    subgraph PostgreSQL
        C1[Company_Login_Details]
        C2[Employee_Details]
        C3[Blog_Posts]
    end

    A1 -->|Form Submit| B1
    A1 -->|Form Submit| B2
    A2 -->|Add Employee| B3
    A3 -->|GET View| B4

    B1 --> C1
    B2 --> C1
    B3 --> C2
    B3 --> C3
    B4 --> C2
    B4 --> C3

    C2 -->|FK| C1
    C3 -->|FK| C1
```
