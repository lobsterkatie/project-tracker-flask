from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def show_home():
    return "YOU ARE HOME. SIT. YOU ARE HOOOOOME."

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get("github", "jhacks")
    first, last, github = hackbright.get_student_by_github(github)
    return "%s is the GitHub account for %s %s" % (github, first, last)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
