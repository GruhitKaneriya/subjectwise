import mysql.connector
from mysql.connector import Error
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session ,jsonify
from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='attendance_management',
            user='root',
            password='gruhit@2004'
        )
        return conn
    except Error as e:
        print(e)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/student', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        roll_no = request.form['rollno']
        password = request.form['password']

        # Authenticate the student using the rollno and password
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE roll_no = %s AND password = %s", (roll_no, password))
        student = cursor.fetchone()

        if student:
            # Store the authenticated student's rollno in session
            session['roll_no'] = roll_no
            return redirect('/subject_selection')
        else:
            flash('Invalid rollno or password. Please try again.')

    return render_template('student_login.html')
@app.route('/subject_selection')
def subject_selection():
    return render_template('subject_selection.html')
@app.route('/app')
def check_app_attendance():
    return check_attendance_for_subject('app')

@app.route('/coa')
def check_coa_attendance():
    return check_attendance_for_subject('coa')

@app.route('/dsa')
def check_dsa_attendance():
    return check_attendance_for_subject('dsa')

@app.route('/os')
def check_os_attendance():
    return check_attendance_for_subject('os')

@app.route('/tbvp')
def check_tbvp_attendance():
    return check_attendance_for_subject('tbvp')

def check_attendance_for_subject(subject):
    roll_no = session.get('roll_no')

    if not roll_no:
        flash('You are not logged in.')
        return redirect('/student')

    conn = create_connection()
    cursor = conn.cursor()

    # Assuming your table for each subject has columns: name, roll_no, date_time
    cursor.execute(f"SELECT * FROM {subject} WHERE roll_no = %s", (roll_no,))
    attendance_record = cursor.fetchone()

    if attendance_record:
        date_time = attendance_record[2].strftime('%Y-%m-%d %H:%M:%S')
        result = f'You were marked present on {date_time}'
    else:
        result = 'You were marked absent.'

    return render_template('attendance_result.html', result=result)
gruhit_image = face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\gruhit.jpg")
gruhit_encoding=face_recognition.face_encodings(gruhit_image)[0]

kushal_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\kushal.jpg")
kushal_encoding=face_recognition.face_encodings(kushal_image)[0]

himanshu_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\himanshu.jpg")
himanshu_encoding=face_recognition.face_encodings(himanshu_image)[0]

sanjay_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\sanjay.jpg")
sanjay_encoding=face_recognition.face_encodings(sanjay_image)[0]

abhishek_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\abhishek.jpg")
abhishek_encoding=face_recognition.face_encodings(abhishek_image)[0]

akul_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\akul.jpg")
akul_encoding=face_recognition.face_encodings(akul_image)[0]

vanshika_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\vanshika.jpg")
vanshika_encoding=face_recognition.face_encodings(vanshika_image)[0]

paras_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\paras.jpg")
paras_encoding=face_recognition.face_encodings(paras_image)[0]

tushar_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\tushar.jpg")
tushar_encoding=face_recognition.face_encodings(tushar_image)[0]

sir_image=face_recognition.load_image_file("C:\\Users\\gdk14\\Desktop\\app project\\images\\sir.jpg")
sir_encoding=face_recognition.face_encodings(sir_image)[0]
known_face_encoding=[
    gruhit_encoding,
    kushal_encoding,
    himanshu_encoding,
    sanjay_encoding,
    abhishek_encoding,
    akul_encoding,
    vanshika_encoding,
    paras_encoding,
    tushar_encoding,
    sir_encoding
]
known_faces_names=[
    "Gruhit",
    "Kushal",
    "Himanshu",
    "Sanjay",
    "Abhishek",
    "Akul",
    "Vanshika",
    "Paras",
    "Tushar",
    "Sir"
]
students=known_faces_names.copy()

# Add roll numbers for each student
known_faces_roll_nos = ['RA2211003010041',
                        'RA2211003010007',
                        'RA2211003010019',
                        'RA2211003010014',
                        'RA2211003010066',
                        'RA2211003010029',
                        'RA2211003010021',
                        'RA2211003010040',
                        'RA2211003010056',
                        'Rajni Fan']

face_locations=[]
face_encodings=[]
face_names=[]
s=True
# Create an empty list to store the names of recognized students
recognized_students = []

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/take_attendance', methods=['GET', 'POST'])
def take_attendance():
    conn = create_connection()
    if request.method == 'POST':
        subject = request.form['subject']
        teacher_id = request.form['teacher_id']
        section = request.form['section']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teacher WHERE subject = %s AND teacher_id = %s AND section = %s", (subject, teacher_id, section))
        teacher = cursor.fetchone()
        if teacher:
            return redirect(url_for('start_attendance', subject=subject))  # Include the subject value in the redirect URL
        else:
            return "Invalid credentials for taking attendance. Please try again."
    return render_template('take_attendance.html')

@app.route('/view_attendance', methods=['GET', 'POST'])
def view_attendance():
    conn = create_connection()
    if request.method == 'POST':
        subject = request.form['subject']
        teacher_id = request.form['teacher_id']
        section = request.form['section']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teacher WHERE subject = %s AND teacher_id = %s AND section = %s", (subject, teacher_id, section))
        teacher = cursor.fetchone()
        if teacher:
            # Fetch present and absent students from the database
            cursor.execute("SELECT name, roll_no FROM student WHERE roll_no IN (SELECT roll_no FROM {})".format(subject))
            present_students = cursor.fetchall()
            cursor.execute("SELECT name, roll_no FROM student WHERE roll_no NOT IN (SELECT roll_no FROM {})".format(subject))
            absent_students = cursor.fetchall()
            print("Present Students:", present_students)
            print("Absent Students:", absent_students)
            return render_template('view_attendance.html', present_students=present_students, absent_students=absent_students)
        else:
            return "Invalid credentials for viewing attendance. Please try again."
    return render_template('view_attendance.html')


@app.route('/start_attendance')
def start_attendance():
    conn = create_connection()  # Assuming this function creates a connection to your database
    subject = request.args.get('subject')
    global recognized_students
    video_capture = cv2.VideoCapture(0)
    s = True
    threshold = 0.6  # Adjust this threshold according to your needs

    while s:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if s:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                face_distances = face_recognition.face_distance(known_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distances)
                if face_distances[best_match_index] < 0.6:
                    name = known_faces_names[best_match_index]
                    recognized_faces_names.append(name)
                else:
                    name = "Not Recognized"
                    recognized_faces_names.append(name)

                if True in matches:
                    best_match_index = np.argmin(face_distance)
                    name = known_faces_names[best_match_index]
                    roll_no = known_faces_roll_nos[best_match_index]
                    print(f"Detected face: {name}, Roll No: {roll_no}")

                    if name not in recognized_students:
                        date_time = datetime.now()
                        entities = (name, roll_no, date_time)
                        insert_values(conn, subject, entities)
                        recognized_students.append(name)
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    for (top, right, bottom, left), name in zip(face_locations, recognized_faces_names):
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


        cv2.imshow("attendance system", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            s = False

    video_capture.release()
    cv2.destroyAllWindows()

    for student in recognized_students:
        date_time = datetime.now()
        roll_no = known_faces_roll_nos[known_faces_names.index(student)]
        entities = (student, roll_no, date_time)
        # Debugging to check data before insertion
        print(f"Data to be inserted: {entities}")

        try:
            insert_values(conn, subject, entities)  # Pass the 'subject' and 'entities' arguments
            recognized_students.remove(student)  # Remove the student after successful insertion
        except Error as e:
            print(f"Error occurred: {e}")

    # Commit once after all insertions
    conn.commit()
    return render_template('attendance_success.html')

def insert_values(conn, subject, values):  # Accept the subject parameter
    try:
        cursor = conn.cursor()
        table_name = subject  # Use the subject value to construct the table name
        query = f"INSERT INTO {table_name} (name, roll_no, date_time) VALUES (%s, %s, %s)"
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
