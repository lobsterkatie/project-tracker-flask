from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)

@app.route("/")
def show_home():
    return render_template("home.html")

@app.route("/student-search")
def get_student_form():
    return render_template("student_search.html")


@app.route("/student")
def redirect_to_student_info():
    """Take form submission and redirect to that student's info page"""
    github = request.args.get("github", "jhacks")
    url_string = "student/" + github
    return redirect(url_string)


@app.route("/student/<string:github>")
def get_student(github):
    """Show information about a student."""

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_all_grades_by_github(github)
    return render_template("student_info.html", first=first, last=last, github=github, grades=grades)


@app.route("/student-add")
def add_student_form():
    """Show a form to add a new student"""
    return render_template("student_add_form.html")


@app.route("/student-add-confirmation", methods=["POST"])
def confirm_student_add():
    """Show a confirmation that student has been added"""
    github = request.form.get("github", "jhacks")
    last = request.form.get("last", "Hacker")
    first = request.form.get("first", "Jane")
    confirmation_string = hackbright.make_new_student(first, last, github)
    return render_template("student_add_confirmation.html", confirmation_string=confirmation_string)

@app.route("/project/<string:title>")
def get_project_info(title):
    """Shows project info given the title"""

    id, title, desc, max_grade = hackbright.get_project_by_title(title)
    grades = hackbright.get_all_grades_by_project(title)
    return render_template("project_info.html", title=title, desc=desc, max_grade=max_grade, grades=grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
