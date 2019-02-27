
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String, nullable = False)
    course_title = db.Column(db.String, nullable = False)

    # Specify any relationship fields.
    students = db.relationship("RegisteredStudent", backref="courses", lazy=True)
    # specify any utility methods associated with the model.
    def add_student(self,name,grade):
        # Notice that we set the foreign key for the passenger class.
        new_student = RegisteredStudent(name=name, grade=grade, id=self.id )
        db.session.add(new_student)
        db.session.commit()

class RegisteredStudent(db.Model):
    __tablename__= "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    grade = db.Column(db.String, nullable = False)
    # Notice, this field serves as a ForeignKey.
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
