from flask import Flask, request, render_template, flash, redirect, url_for
import psycopg
from dotenv import load_dotenv
import os

# --------------------------------------------------------------
# Step 1: Load environment variables from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# --------------------------------------------------------------
# Step 2: Connect to PostgreSQL
try:
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()
except psycopg.Error as e:
    print(f"❌ Database connection failed: {e}")
    exit()

# --------------------------------------------------------------
# Step 3: Initialize Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") # Secret key for session management
#-----------------------------------------------------------------------------------------------------------------------------------
# Define the routes for the Flask application
#-----------------------------------------------------------------------------------------------------------------------------------

# Home route
@app.route('/')
def home():
    return render_template('home.html')
#-----------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------------
# Login Route
username = ""  # Initialize username variable to store the logged-in user's username
#-----------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    global conn, cursor, username
#-----------------------------------------------------------------------------------------------------------------------------------
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
#-----------------------------------------------------------------------------------------------------------------------------------
        #Check if the username and password match an existing user
        SelectStatement='''SELECT * FROM "Company_Login_Details" WHERE "Username" = %s AND "Password" = %s'''
        cursor.execute(SelectStatement, (username, password))
        conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
        Fetch = cursor.fetchall()
        conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
        # If a match is found, redirect to the dashboard
        if Fetch != []:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        # If no match is found, show an error message
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))
#-----------------------------------------------------------------------------------------------------------------------------------
       

# Register Route
#-----------------------------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    global conn, cursor
#-----------------------------------------------------------------------------------------------------------------------------------
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
#-----------------------------------------------------------------------------------------------------------------------------------
        username = request.form.get('username')
        password = request.form.get('password')
#-----------------------------------------------------------------------------------------------------------------------------------
        SelectStatement='''SELECT * FROM "Company_Login_Details" WHERE "Username" = %s'''
        cursor.execute(SelectStatement,(username,))
        conn.commit()

        # Check if the username already exists
        Fetch=cursor.fetchall()
        if Fetch!=[]:
            flash('Username already exists. Please choose a different one.', 'warning') # Use category 'warning'
            return render_template('register.html')
        # If the username does not exist, insert the new user
#-----------------------------------------------------------------------------------------------------------------------------------
        Statement='''INSERT INTO "Company_Login_Details"("Username","Password") 
                          SELECT new_data.Username, new_data.Password
                          FROM (VALUES (%s, %s)) AS new_data(Username, Password)
                          WHERE NOT EXISTS(SELECT 1 FROM "Company_Login_Details" WHERE "Username" = new_data.Username)'''
        cursor.execute(Statement,(username, password))
        conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
        SelectStatement='''SELECT * FROM "Company_Login_Details" WHERE "Username" = %s'''
        cursor.execute(SelectStatement,(username,))
        conn.commit()
        Fetch=cursor.fetchall()
        if Fetch !=[]:
            return render_template('thankyou.html')    
#-----------------------------------------------------------------------------------------------------------------------------------


#Dashboard Route
#-----------------------------------------------------------------------------------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
#-----------------------------------------------------------------------------------------------------------------------------------


#View Records Route
#-----------------------------------------------------------------------------------------------------------------------------------
@app.route('/view')
def view_records():
    global conn, cursor 
    # Fetch all records from the "Employee" table which has the same Company ID as the logged in user 
#-----------------------------------------------------------------------------------------------------------------------------------
    # Fetch the Company ID of the logged-in user
    CompanyIDStatement= '''SELECT "Company_ID" FROM "Company_Login_Details" WHERE "Username" = %s'''
    cursor.execute(CompanyIDStatement, (username,))
    conn.commit()
    result = cursor.fetchall()
    conn.commit()
    CompanyID= result[0][0]
#-----------------------------------------------------------------------------------------------------------------------------------
    # Validate the input data
    SelectStatement = ''' SELECT "Employee_ID","FullName", "Department_ID" FROM "Employee_Details" WHERE "Company_ID" = %s '''
    cursor.execute(SelectStatement, (CompanyID,))
    conn.commit()
    # Fetch the results
    records = cursor.fetchall()
    conn.commit()
    
    if result:
        # Convert to list of dicts
        employees = [{'id': r[0], 'name': r[1], 'department': r[2]} for r in records]
        return render_template('view.html', employees=employees)
    else:
        flash('No records found for the logged-in user.', 'info')
        return render_template('view.html', employees=[])
    
#-----------------------------------------------------------------------------------------------------------------------------------


#Add Department Route
#-----------------------------------------------------------------------------------------------------------------------------------
@app.route('/department', methods=['GET', 'POST'])
def add_department():
    global conn, cursor, username
#-----------------------------------------------------------------------------------------------------------------------------------
    department= request.form.get('deptName')
    description= request.form.get('deptdesc')
    if request.method == "GET":
        return render_template('department.html')
    elif request.method == "POST":
#-----------------------------------------------------------------------------------------------------------------------------------
        # Fetch the Company ID of the logged-in user
        CompanyIDStatement= '''SELECT "Company_ID" FROM "Company_Login_Details" WHERE "Username" = %s'''
        cursor.execute(CompanyIDStatement, (username,))
        conn.commit()
        result = cursor.fetchall()
        conn.commit()
        if result:
            CompanyID= result[0][0]
#-----------------------------------------------------------------------------------------------------------------------------------
        # Validate the input data
        SelectStatement='''SELECT * FROM "Departments" WHERE "DepartmentName" = %s AND "Company_ID" = %s'''
        cursor.execute(SelectStatement,(department,CompanyID))
        conn.commit()
        # Check if the department already exists
        # Fetch the results
        Fetch = cursor.fetchall()
        conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
        if Fetch != []:
            flash('Department already exists. Please enter a different name.', 'warning')
            return render_template('department.html')
#-----------------------------------------------------------------------------------------------------------------------------------
        else:
            # Insert the new department into the "Department" table
            Statement = '''INSERT INTO "Departments"("DepartmentName", "DepartmentDescription", "Company_ID") VALUES (%s, %s, %s)'''
            cursor.execute(Statement, (department, description, CompanyID))
            conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
            # Select the Specific Department
            SelectStatement=  '''SELECT * FROM "Departments" WHERE "DepartmentName" = %s AND "Company_ID" = %s'''
            cursor.execute(SelectStatement,(department,CompanyID))
            conn.commit()
            # Fetch the results again to check if the insert was successful
            Fetch=cursor.fetchall()
            conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
            if Fetch != []:
                flash('Department added successfully! Add More if required!', 'success')
                return render_template('department.html')
            else:
                # After insertion
                flash('Department wasn not added! Try Again', 'success')
                return render_template('department.html')
#-----------------------------------------------------------------------------------------------------------------------------------


#Add Employee Route
#-----------------------------------------------------------------------------------------------------------------------------------
@app.route('/employee', methods=['GET', 'POST'])
def add_employee():
    global conn, cursor, username
#-----------------------------------------------------------------------------------------------------------------------------------
    # This function will handle the addition of a new employee
    fullName = request.form.get('fullName')
    department= request.form.get('department')

    if request.method == "GET":
        return render_template('employee.html')
    elif request.method == "POST":
#-----------------------------------------------------------------------------------------------------------------------------------
        # Fetch the Company ID of the logged-in user
        CompanyIDStatement= '''SELECT "Company_ID" FROM "Company_Login_Details" WHERE "Username" = %s'''
        cursor.execute(CompanyIDStatement, (username,))
        conn.commit()
        result = cursor.fetchall()
        conn.commit()
        if result !=[]:
            CompanyID= result[0][0]
        print(CompanyID)
#-----------------------------------------------------------------------------------------------------------------------------------
        # Validate the input data
        SelectStatement='''SELECT * FROM "Employee_Details" WHERE "FullName" = %s AND "Company_ID" = %s'''
        cursor.execute(SelectStatement,(fullName,CompanyID))
        conn.commit()
        # Check if the employee already exists
        # Fetch the results
        Fetch = cursor.fetchall()
        conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
        if Fetch != []:
            flash('Employee already exists. Please enter a different name.', 'warning')
            return render_template('employee.html')
#-----------------------------------------------------------------------------------------------------------------------------------
        else:
            #Fetch the Department ID of the department entered by the user according to the Company ID
            DepartmentIDStatement = '''SELECT "Department_ID" FROM "Departments" WHERE  "DepartmentName" = %s AND "Company_ID" = %s'''
            cursor.execute(DepartmentIDStatement, (department, CompanyID))
            conn.commit()
            result = cursor.fetchall()
            conn.commit()
            if result != []:
                departmentID = result[0][0]
            else:
                flash("⚠️ Department not found. Please check the name.", "danger")
                return render_template("employee.html")
#----------------------------------------------------------------------------------------------------------------------------------
            # Insert the new employee into the "Employee" table
            Statement = '''INSERT INTO "Employee_Details"("FullName", "Department_ID","Company_ID") VALUES (%s, %s, %s)'''
            cursor.execute(Statement, (fullName, departmentID, CompanyID))
            conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
            # Select the Specific Employee's Detail
            SelectStatement=  '''SELECT * FROM "Employee_Details" WHERE "FullName" = %s AND "Company_ID" = %s'''
            cursor.execute(SelectStatement,(fullName,CompanyID))
            conn.commit()
            # Fetch the results again to check if the insert was successful
            Fetch=cursor.fetchall()
            conn.commit()
#-----------------------------------------------------------------------------------------------------------------------------------
            if Fetch !=[]:
                flash('Employee added successfully! Add More if required!', 'success')
                return render_template('employee.html')    
#-----------------------------------------------------------------------------------------------------------------------------------
            else:
                flash('Failed to add employee. Please try again.', 'danger')
                return render_template('employee.html')
#-----------------------------------------------------------------------------------------------------------------------------------


# Login Route
#-----------------------------------------------------------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    global username
    username = ""  # Reset the global username
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))
#-----------------------------------------------------------------------------------------------------------------------------------


#Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)    
    
