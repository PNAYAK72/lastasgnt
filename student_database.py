#!/usr/bin/env python3
import cgi
import sqlite3


# Function to calculate the average score
def calculate_average(midterm_exam1, midterm_exam2, final_exam):
    return (midterm_exam1 + midterm_exam2 + 2 * final_exam) / 4

# Connect to the database
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# Create the 'student_grades' table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS student_grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    midterm_exam1 REAL NOT NULL,
                    midterm_exam2 REAL NOT NULL,
                    final_exam REAL NOT NULL
                )''')

# Commit changes to the database
conn.commit()

# HTML header
print("Content-type: text/html\n")

# Get form data
form = cgi.FieldStorage()

# Check if the form is submitted
if "submit" in form:
    # Get form data
    name = form.getvalue("name")
    midterm_exam1 = float(form.getvalue("midterm_exam1"))
    midterm_exam2 = float(form.getvalue("midterm_exam2"))
    final_exam = float(form.getvalue("final_exam"))
    
    # Calculate average score
    average_score = calculate_average(midterm_exam1, midterm_exam2, final_exam)
    
    # Insert the data into the database
    cursor.execute('''INSERT INTO student_grades (name, midterm_exam1, midterm_exam2, final_exam)
                      VALUES (?, ?, ?, ?)''', (name, midterm_exam1, midterm_exam2, final_exam))
    
    # Commit the changes to the database
    conn.commit()

# Print the HTML form
print('''
<!DOCTYPE html>
<html>
<head>
    <title>Student Database</title>
</head>
<body>
    <h1>Student Database</h1>
    <form method="post">
        <label for="name">Name:</label>
        <input type="text" name="name" required><br>
        <label for="midterm_exam1">Midterm Exam 1:</label>
        <input type="number" name="midterm_exam1" required><br>
        <label for="midterm_exam2">Midterm Exam 2:</label>
        <input type="number" name="midterm_exam2" required><br>
        <label for="final_exam">Final Exam:</label>
        <input type="number" name="final_exam" required><br>
        <input type="submit" name="submit" value="Add Student">
    </form>
    <br>
    <h2>Student Records</h2>
    <table border="1">
        <tr>
            <th>Name</th>
            <th>Midterm Exam 1</th>
            <th>Midterm Exam 2</th>
            <th>Final Exam</th>
            <th>Average Score</th>
        </tr>
''')


# Retrieve data from the database and display it in the table
cursor.execute("SELECT name, midterm_exam1, midterm_exam2, final_exam FROM student_grades")
rows = cursor.fetchall()

for row in rows:
    name, midterm_exam1, midterm_exam2, final_exam = row
    average_score = calculate_average(midterm_exam1, midterm_exam2, final_exam)

    print(f'''
        <tr>
            <td>{name}</td>
            <td>{midterm_exam1}</td>
            <td>{midterm_exam2}</td>
            <td>{final_exam}</td>
            <td>{average_score:.2f}</td>
        </tr>
    ''')
# Close the database connection
conn.close()

# HTML footer
print('''
    </table>
</body>
</html>
''')
