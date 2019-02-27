# Import appropriate libraries,
import sys
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# This module defines that database parameters.
from config import Config
# Load the models (i.e. Course, Student model classes)
from models import *

# Define an instance of flask application, load database parameters.
app = Flask(__name__)
app.config.from_object(Config)

# Display a welcome message,
# Lists all current courses in the database.
# When a user clicks a course from the list it should be redirected to the route
# /register_student/<int:course_id>
# Provide a form for the user to add new course.
# When a user submit this form it should be redirected to the route /add_course
@app.route("/")
def index():
    # Equivalent to: "SELECT * from course" SQL statement.
    course = Course.query.all()
    return render_template('index.html', course=course)

# Handle post requests only.
# Obtain in information about the course as submitted by the course form.
# Add the course to the database using the Course model.
@app.route("/add_course",methods=["post"])
def add_course():
    # Get information from the form.
    course_title = request.form.get("course_title")
    course_number = request.form.get("course_number")
    # Equivalent to:
    # INSERT INTO course (course_title, course_number) VALUES (origin,...)
    course = Course(course_title=course_title, course_number=course_number)
    db.session.add(course)
    db.session.commit()
    # Query database.
    course = Course.query.all()
    return render_template('index.html', course=course)

# '/register_student/' This route should handle both GET and POST requests, as follows:
# GET REQUEST:
# Queries the database to obtain all information about the course with id==course_id
# and all current registered students in the course.
# renders the template course_details.html . The template should show information
# about the course, a listing of all students registered and a form for users to register
# new student. When a user submit this form it should be redirected to the route
@app.route("/register_student/<int:course_id>", methods=["GET", "POST"])
def book_flight(course_id):
    # Equivalent to "SELECT * from course where id=course_id"
    course = Course.query.get(course_id)
    # If this is a post request = Register the student.
    if request.method == 'POST':
        name = request.form.get("name")
        grade = request.form.get("grade")
        # Use the utility method to add a new student in the database.
        course.add_student(name,grade)
    # Use the relationships field in the course model to retrieve
    # all students in the current course.
    students = course.students
    return render_template("course_details.html", course=course, students=students)

def main():
    if (len(sys.argv)==2):
        print(sys.argv)
        if sys.argv[1] == 'createdb':
            db.create_all()
        else:
            print("Run app using 'flask run'")
            print("To create a database use 'python app.py createdb")
# Run the main method in the context of our flass application
# This allows db know about our models.
if __name__ == "__main__":
    with app.app_context():
        main()
