from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Kashif7kato'
app.config['MYSQL_DB'] = 'restaurant_management'

# Initialize MySQL
db = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace this with your authentication logic
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT username, password FROM login WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and password == user[1]:  # Use integer index to access 'password' column
            # Successful login
            return redirect('/homepage')
        else:
            # Failed login
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already exists. Please choose another username."
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, password))
            db.connection.commit()
            cursor.close()
            return "Registration successful. You can now log in."

    return render_template('register.html')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Handle POST requests for the homepage if needed
        pass
    return render_template('homepage.html')

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    if request.method == 'POST':
        # Handle staff-related operations here, e.g., adding new staff
        staff_name = request.form['staff_name']
        staff_number = request.form['staff_number']
        staff_designation = request.form['staff_designation']
        staff_salary = request.form['staff_salary']
        
        # Insert the new staff into the database
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO staff (staff_name, staff_number, staff_designation, staff_salary) VALUES (%s, %s, %s, %s)",
                       (staff_name, staff_number, staff_designation, staff_salary))
        db.connection.commit()
        cursor.close()
    
    # Fetch the list of staff from the database to display in the template
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM staff")
    staff_data = cursor.fetchall()
    cursor.close()

    return render_template('staff.html', staff=staff_data)

@app.route('/add_staff', methods=['POST'])
def add_staff():
    if request.method == 'POST':
        staff_name = request.form['staff_name']
        staff_number = request.form['staff_number']
        staff_designation = request.form['staff_designation']
        staff_salary = request.form['staff_salary']

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO staff (staff_name, staff_number, staff_designation, staff_salary) VALUES (%s, %s, %s, %s)",
                       (staff_name, staff_number, staff_designation, staff_salary))
        db.connection.commit()
        cursor.close()

    return redirect('/staff')

@app.route('/update_staff', methods=['POST'])
def update_staff():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        staff_name = request.form['staff_name']
        staff_number = request.form['staff_number']
        staff_designation = request.form['staff_designation']
        staff_salary = request.form['staff_salary']

        cursor = db.connection.cursor()
        cursor.execute("UPDATE staff SET staff_name = %s, staff_number = %s, staff_designation = %s, staff_salary = %s WHERE staff_id = %s", (staff_name, staff_number, staff_designation, staff_salary, staff_id))
        db.connection.commit()
        cursor.close()

    return redirect('/staff')

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        if 'add_customer' in request.form:
            # Handle adding a new customer
            customer_name = request.form['customer_name']
            customer_number = request.form['customer_number']
            customer_email = request.form['customer_email']
            customer_address = request.form['customer_address']

            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO customer (customer_name, customer_number, customer_email, customer_address) VALUES (%s, %s, %s, %s)", (customer_name, customer_number, customer_email, customer_address))
            db.connection.commit()
            cursor.close()

        elif 'delete_customer' in request.form:
            # Handle deleting a customer
            customer_id = request.form['customer_id']

            cursor = db.connection.cursor()
            cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
            db.connection.commit()
            cursor.close()

    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM customer")
    customer_data = cursor.fetchall()
    cursor.close()

    return render_template('customers.html', customers=customer_data)

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Get user input from the form
        reservation_date = request.form['reservation_date']
        party_size = request.form['party_size']
        customer_id = request.form['customer_id']
        table_id = request.form['table_id']

        # Insert reservation into the database
        cursor = db.connection.cursor()
        cursor.execute(
            "INSERT INTO reservation (reservation_date, party_size, table_id, customer_id) VALUES (%s, %s, %s, %s)",
            (reservation_date, party_size, table_id, customer_id)
        )
        db.connection.commit()
        cursor.close()

    # Fetch reservations for display
    cursor = db.connection.cursor()
    cursor.execute(
        "SELECT r.reservation_id, r.reservation_date, r.party_size, r.customer_id, r.table_id, t.waiter_id "
        "FROM reservation r "
        "LEFT JOIN table_assignments t ON r.table_id = t.table_id"
    )
    reservations = cursor.fetchall()
    cursor.close()

    # Fetch customers and tables for dropdown options
    customers = get_customers()
    tables = get_tables()

    return render_template('reservation.html', customers=customers, tables=tables, reservations=reservations)

def get_customers():
    cursor = db.connection.cursor()
    cursor.execute("SELECT customer_id, customer_name FROM customer")
    customers = cursor.fetchall()
    cursor.close()
    return customers

def get_tables():
    cursor = db.connection.cursor()
    cursor.execute("SELECT table_id, employee_capacity FROM table_")
    tables = cursor.fetchall()
    cursor.close()
    return tables

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        if 'add_menu' in request.form:
            # Handle adding a new menu item
            menu_name = request.form['menu_name']
            menu_price = request.form['menu_price']

            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO menu (menu_name, menu_price) VALUES (%s, %s)", (menu_name, menu_price))
            db.connection.commit()
            cursor.close()

        elif 'delete_menu' in request.form:
            # Handle deleting a menu item
            menu_id = request.form['menu_id']
            cursor = db.connection.cursor()
            cursor.execute("DELETE FROM menu WHERE menu_id = %s", (menu_id,))
            db.connection.commit()
            cursor.close()

    # Fetch menu items
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_data = cursor.fetchall()
    cursor.close()

    return render_template('menu.html', menu=menu_data)
   
@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        if 'add_review' in request.form:
            customer_id = request.form['customer_id']
            staff_id = request.form['staff_id']
            review_text = request.form['review_text']

            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO staff_review (customer_id, staff_id,review_text ) VALUES (%s,%s,%s)", (customer_id, staff_id,review_text))
            db.connection.commit()
            cursor.close()

            return redirect('/review')

    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM staff_review")
    tables_data = cursor.fetchall()
    cursor.close()

    return render_template('review.html', tables_data=tables_data)      
          
@app.route('/table', methods=['GET', 'POST'])
def tables():
    if request.method == 'POST':
        if 'add_table' in request.form:
            employee_capacity = request.form['employee_capacity']
            employee_booking = request.form['employee_booking']

            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO table_ (employee_capacity, employee_booking) VALUES (%s, %s)", (employee_capacity, employee_booking))
            db.connection.commit()
            cursor.close()

            # Redirect to the same page after handling the form
            return redirect('/table')

        elif 'delete_table' in request.form:
            table_id = request.form['table_id']

            cursor = db.connection.cursor()

            try:
                # Delete reservations associated with the table
                cursor.execute("DELETE FROM reservation WHERE table_id = %s", (table_id,))

                # Then, delete the table itself
                cursor.execute("DELETE FROM table_ WHERE table_id = %s", (table_id,))

                db.connection.commit()
            except Exception as e:
                print(f"Error: {e}")
                db.connection.rollback()
            finally:
                cursor.close()

            # Redirect back to the /table route after deleting
            return redirect('/table')

    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM table_")
    tables_data = cursor.fetchall()
    cursor.close()

    return render_template('table.html', tables_data=tables_data)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        if 'add_order' in request.form:
            menu_id = request.form['menu_id']
            special_request = request.form['special_request']
            order_quantity = request.form['order_quantity']
            customer_id = request.form['customer_id']

            # Retrieve additional information about the menu item
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM menu WHERE menu_id = %s", (menu_id,))
            menu_info = cursor.fetchone()

            # Add the order to the database
            cursor.execute("""
    INSERT INTO order_ (menu_id, special_request, order_quantity, customer_id, table_assignment_id, chef_id)
    VALUES (
        %s,
        %s,
        %s,
        %s,
        (SELECT assignment_id FROM table_assignments WHERE waiter_id IS NOT NULL LIMIT 1),
        (SELECT staff_id FROM staff WHERE staff_designation = 'chef' LIMIT 1)
    )
""", (
    int(menu_id) if menu_id else None,
    special_request,
    int(order_quantity) if order_quantity else None,
    int(customer_id) if customer_id else None
))


            db.connection.commit()
            cursor.close()

    # Fetch order information including related data (menu, table, waiter, etc.)
    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT
            o.order_id,
            o.special_request,
            o.order_quantity,
            o.customer_id,
            t.table_id,
            t.waiter_id,
            m.menu_name,
            m.menu_price
        FROM
            order_ o
            LEFT JOIN table_assignments t ON o.table_assignment_id = t.assignment_id
            LEFT JOIN menu m ON o.menu_id = m.menu_id
    """)
    orders_data = cursor.fetchall()
    cursor.close()

    # Fetch menu information
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_data = cursor.fetchall()
    cursor.close()

    return render_template('order.html', menu=menu_data, order=orders_data)



if __name__ == "__main__":
    app.run(debug=True)
