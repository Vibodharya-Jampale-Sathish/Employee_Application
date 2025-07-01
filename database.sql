-- Company Login Details Table
CREATE TABLE "Company_Login_Details" (
    "Company_ID" SERIAL PRIMARY KEY,
    "Username" VARCHAR(100) UNIQUE NOT NULL,
    "Password" VARCHAR(100) NOT NULL
);

-- Departments Table
CREATE TABLE "Departments" (
    "Department_ID" SERIAL PRIMARY KEY,
    "Company_ID" INTEGER NOT NULL REFERENCES "Company_Login_Details"("Company_ID") ON DELETE CASCADE,
    "DepartmentName" VARCHAR(100) NOT NULL,
    "DepartmentDescription" TEXT
);

-- Employee Details Table
CREATE TABLE "Employee_Details" (
    "Employee_ID" SERIAL PRIMARY KEY,
    "Company_ID" INTEGER NOT NULL REFERENCES "Company_Login_Details"("Company_ID") ON DELETE CASCADE,
    "Department_ID" INTEGER NOT NULL REFERENCES "Departments"("Department_ID") ON DELETE SET NULL,
    "FullName" VARCHAR(150) NOT NULL
);
