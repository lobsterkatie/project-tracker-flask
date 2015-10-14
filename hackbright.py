"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackbright.db'
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github})
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])
    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (:first_name, :last_name, :github)"""
    db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name, 'github': github})
    db.session.commit()
    confirmation_string = "Successfully added student: %s %s" % (first_name, last_name)
    print confirmation_string, "in hackbright.py"
    return confirmation_string


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT *
        FROM projects
        WHERE title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()
    print "ID: {} \nTitle: {} \nDescription: {}\nMax Grade: {}".format(row[0], row[1], row[2], row[3])
    return row


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    
    QUERY = """
        SELECT grade
        FROM Grades
        WHERE student_github = :github
            AND project_title = :title
        """

    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})
    row = db_cursor.fetchone()
    print "Grade on {project}: {grade}".format(project=title, grade=row[0])
    return row


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    QUERY = """INSERT INTO Grades VALUES (:github, :title, :grade)"""
    db.session.execute(QUERY, {'github': github, 'title': title, 'grade': grade})
    db.session.commit()
    confirmation_string = "Successfully added grade {} for student {} on project {} ".format(grade, github, title)
    print confirmation_string
    return confirmation_string


def get_all_grades_by_github(github):
    """Given a github username, returns all project grades for that student"""

    QUERY = """SELECT project_title, grade FROM Grades WHERE student_github = :github"""
    db_cursor = db.session.execute(QUERY, {'github': github})
    return db_cursor

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        if input_string != "":
            tokens = input_string.split()
            command = tokens[0]
            args = tokens[1:]

            if command == "get_student":
                github = args[0]
                get_student_by_github(github)

            elif command == "assign_grade":
                github = args[0]
                title = args[1]
                grade = args[2]
                assign_grade(github, title, grade)

            elif command == "get_project":
                title = args[0]
                get_project_by_title(title)

            elif command == "get_grade":
                github = args[0]
                title = args[1]
                get_grade_by_github_title(github, title)

            elif command == "new_student":
                first_name, last_name, github = args   # unpack!
                make_new_student(first_name, last_name, github)

            else:
                if command != "quit":
                    print "Invalid Entry. Try again."


if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db.session.close()
