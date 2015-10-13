from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get("github", "jhacks")
    first, last, github = hackbright.get_student_by_github(github)
    return render_template("student_info.html", first=first, last=last, github=github)


@app.route("/student-add")
def add_student_form():
    return render_template("student_add_form.html")


@app.route("/student-add-confirmation", methods=["POST"])
def confirm_student_add():
    github = request.form.get("github")
    last = request.form.get("last")
    first = request.form.get("first")
    confirmation_string = hackbright.make_new_student(first, last, github)
    return render_template("student_add_confirmation.html", confirmation_string=confirmation_string)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
