from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="varunesh1",
        database="employee_db"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO employees (name, email, department, salary) VALUES (%s,%s,%s,%s)",
            (name, email, department, salary)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    return render_template('add_employee.html')

@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']

        cursor.execute(
            """
            UPDATE employees
            SET name=%s, email=%s, department=%s, salary=%s
            WHERE id=%s
            """,
            (name, email, department, salary, id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/')

    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit_employee.html', employee=employee)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
