
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'devsecretkey')

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'Avdhi@2005')
DB_NAME = os.environ.get('DB_NAME', 'hospital_db')

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def list_patients():
    con = get_conn()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT p.id, p.name, p.age, p.gender, p.disease, r.room_number AS room_no, d.name AS doctor_name
        FROM patients p
        LEFT JOIN rooms r ON p.room_id = r.id
        LEFT JOIN doctors d ON p.doctor_id = d.id
        ORDER BY p.id
    """)
    patients = cur.fetchall()
    con.close()
    return render_template('patients/list.html', patients=patients)

@app.route('/patients/add', methods=['GET','POST'])
def add_patient():
    con = get_conn()
    cur = con.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form.get('age') or None
        gender = request.form.get('gender') or None
        disease = request.form.get('disease') or None
        room_id = request.form.get('room_id') or None
        doctor_id = request.form.get('doctor_id') or None
        cur.execute("INSERT INTO patients (name, age, gender, disease, room_id, doctor_id) VALUES (%s,%s,%s,%s,%s,%s)",
                    (name, age, gender, disease, room_id, doctor_id))
        con.commit()
        con.close()
        flash('Patient added.', 'success')
        return redirect(url_for('list_patients'))
    cur.execute("SELECT id, room_number FROM rooms")
    rooms = cur.fetchall()
    cur.execute("SELECT id, name FROM doctors")
    doctors = cur.fetchall()
    con.close()
    return render_template('patients/add.html', rooms=rooms, doctors=doctors)

@app.route('/patients/edit/<int:id>', methods=['GET','POST'])
def edit_patient(id):
    con = get_conn()
    cur = con.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form.get('age') or None
        gender = request.form.get('gender') or None
        disease = request.form.get('disease') or None
        room_id = request.form.get('room_id') or None
        doctor_id = request.form.get('doctor_id') or None
        cur.execute("UPDATE patients SET name=%s, age=%s, gender=%s, disease=%s, room_id=%s, doctor_id=%s WHERE id=%s",
                    (name, age, gender, disease, room_id, doctor_id, id))
        con.commit()
        con.close()
        flash('Patient updated.', 'success')
        return redirect(url_for('list_patients'))
    cur.execute("SELECT * FROM patients WHERE id=%s", (id,))
    patient = cur.fetchone()
    cur.execute("SELECT id, room_number FROM rooms")
    rooms = cur.fetchall()
    cur.execute("SELECT id, name FROM doctors")
    doctors = cur.fetchall()
    con.close()
    return render_template('patients/edit.html', patient=patient, rooms=rooms, doctors=doctors)

@app.route('/patients/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    con = get_conn()
    cur = con.cursor()
    cur.execute("DELETE FROM patients WHERE id=%s", (id,))
    con.commit()
    con.close()
    flash('Patient deleted.', 'info')
    return redirect(url_for('list_patients'))

@app.route('/doctors')
def list_doctors():
    con = get_conn()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM doctors ORDER BY id")
    doctors = cur.fetchall()
    con.close()
    return render_template('doctors/list.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET','POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        spec = request.form.get('specialization') or None
        phone = request.form.get('phone') or None
        con = get_conn()
        cur = con.cursor()
        cur.execute("INSERT INTO doctors (name, specialization, phone) VALUES (%s,%s,%s)", (name, spec, phone))
        con.commit()
        con.close()
        flash('Doctor added.', 'success')
        return redirect(url_for('list_doctors'))
    return render_template('doctors/add.html')

@app.route('/doctors/edit/<int:id>', methods=['GET','POST'])
def edit_doctor(id):
    con = get_conn()
    cur = con.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        spec = request.form.get('specialization') or None
        phone = request.form.get('phone') or None
        cur.execute("UPDATE doctors SET name=%s, specialization=%s, phone=%s WHERE id=%s", (name, spec, phone, id))
        con.commit()
        con.close()
        flash('Doctor updated.', 'success')
        return redirect(url_for('list_doctors'))
    cur.execute("SELECT * FROM doctors WHERE id=%s", (id,))
    doctor = cur.fetchone()
    con.close()
    return render_template('doctors/edit.html', doctor=doctor)

@app.route('/doctors/delete/<int:id>', methods=['POST'])
def delete_doctor(id):
    con = get_conn()
    cur = con.cursor()
    cur.execute("UPDATE patients SET doctor_id = NULL WHERE doctor_id = %s", (id,))
    cur.execute("DELETE FROM doctors WHERE id=%s", (id,))
    con.commit()
    con.close()
    flash('Doctor deleted.', 'info')
    return redirect(url_for('list_doctors'))

@app.route('/rooms')
def list_rooms():
    con = get_conn()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM rooms ORDER BY id")
    rooms = cur.fetchall()
    con.close()
    return render_template('rooms/list.html', rooms=rooms)

@app.route('/rooms/add', methods=['GET','POST'])
def add_room():
    if request.method == 'POST':
        room_no = request.form['room_number']
        rtype = request.form.get('type') or None
        status = request.form.get('status') or None
        con = get_conn()
        cur = con.cursor()
        cur.execute("INSERT INTO rooms (room_number, type, status) VALUES (%s,%s,%s)", (room_no, rtype, status))
        con.commit()
        con.close()
        flash('Room added.', 'success')
        return redirect(url_for('list_rooms'))
    return render_template('rooms/add.html')

@app.route('/rooms/edit/<int:id>', methods=['GET','POST'])
def edit_room(id):
    con = get_conn()
    cur = con.cursor(dictionary=True)
    if request.method == 'POST':
        room_no = request.form['room_number']
        rtype = request.form.get('type') or None
        status = request.form.get('status') or None
        cur.execute("UPDATE rooms SET room_number=%s, type=%s, status=%s WHERE id=%s", (room_no, rtype, status, id))
        con.commit()
        con.close()
        flash('Room updated.', 'success')
        return redirect(url_for('list_rooms'))
    cur.execute("SELECT * FROM rooms WHERE id=%s", (id,))
    room = cur.fetchone()
    con.close()
    return render_template('rooms/edit.html', room=room)

@app.route('/rooms/delete/<int:id>', methods=['POST'])
def delete_room(id):
    con = get_conn()
    cur = con.cursor()
    cur.execute("UPDATE patients SET room_id = NULL WHERE room_id = %s", (id,))
    cur.execute("DELETE FROM rooms WHERE id=%s", (id,))
    con.commit()
    con.close()
    flash('Room deleted.', 'info')
    return redirect(url_for('list_rooms'))

@app.route('/report')
def report():
    con = get_conn()
    cur = con.cursor(dictionary=True)
    cur.execute("""
        SELECT p.name AS patient_name, p.age, p.gender, p.disease, r.room_number, d.name AS doctor_name
        FROM patients p
        LEFT JOIN rooms r ON p.room_id = r.id
        LEFT JOIN doctors d ON p.doctor_id = d.id
        ORDER BY p.id
    """)
    data = cur.fetchall()
    con.close()
    return render_template('report.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
