from flask import Flask, request,render_template,flash
import psycopg2

#Using psycopg2 to connect to a PostgreSQL database
#Make sure to install psycopg2 with pip install psycopg2
conn=None 
try:
    conn = psycopg2.connect(host='localhost', dbname='employee_app', user='postgres', password='131106', port='5432')
    cursor = conn.cursor()
except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")
    # In a real app, you'd handle this more gracefully, maybe exit or show an error page.
    exit()    
app= Flask(__name__)
app.secret_key = 'EmployeeAppSecretKey2006'  # Set a secret key for session management and flash messages
#-----------------------------------------------------------------------------------------------------------------------------------
# Define the routes for the Flask application

@app.route('/')
def home():
    global conn, cursor
#-----------------------------------------------------------------------------------------------------------------------------------
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])

def login():
    global conn, cursor
#-----------------------------------------------------------------------------------------------------------------------------------
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        cursor.execute("SELECT ")

@app.route('/register', methods=['GET', 'POST'])

def register():
    global conn, cursor
#-----------------------------------------------------------------------------------------------------------------------------------
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        print(username, password)
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
       #This Doesn't work
        SelectStatement='''SELECT * FROM "Company_Login_Details" WHERE "Username" = %s'''
        cursor.execute(SelectStatement,(username,))
        conn.commit()
        Fetch=cursor.fetchall()
        if Fetch !=[]:
            return render_template('thankyou.html')    
            # If the insert was successful, commit the transaction
#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)    