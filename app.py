from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "carleton_secret_key"

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def get_logged_in_user():
    username = session.get("username")

    if not username:
        return None

    users = load_users()

    for user in users:
        if user["username"] == username:
            return user

    return None


def require_login():
    user = get_logged_in_user()
    if not user:
        return None, redirect(url_for("login"))
    return user, None


@app.route("/")
def home():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["username"] = user["username"]
                return redirect(url_for("home"))

        return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html", error=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/edit-address", methods=["GET", "POST"])
def edit_address():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response

    if request.method == "POST":
        new_address = request.form.get("address", "").strip()

        users = load_users()
        for saved_user in users:
            if saved_user["username"] == user["username"]:
                saved_user["address"] = new_address
                break

        save_users(users)
        return redirect(url_for("home"))

    return render_template("edit_address.html", user=user)


@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response

    error = None
    success = None

    if request.method == "POST":
        current_password = request.form.get("current-password", "")
        new_password = request.form.get("new-password", "")
        confirm_password = request.form.get("confirm-password", "")

        if current_password != user["password"]:
            error = "Current password is incorrect."
        elif new_password != confirm_password:
            error = "New passwords do not match."
        elif len(new_password) < 6:
            error = "Password must be at least 6 characters."
        else:
            users = load_users()
            for saved_user in users:
                if saved_user["username"] == user["username"]:
                    saved_user["password"] = new_password
                    break

            save_users(users)
            success = "Password updated successfully."
            user = get_logged_in_user()

    return render_template("change_password.html", user=user, error=error, success=success)


@app.route("/personal-data")
def personal_data():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("personal_data.html", user=user)


@app.route("/grades")
def grades():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("grades.html", user=user)


@app.route("/transcript-request")
def transcript_request():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("transcript.html", user=user)


@app.route("/enrollment-verification")
def enrollment_verification():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("enrollment_verification.html", user=user)


@app.route("/search-courses")
def search_courses():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("search_courses.html", user=user)


@app.route("/add-drop")
def add_drop():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("add_drop.html", user=user)


@app.route("/schedule")
def schedule():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("schedule.html", user=user)


@app.route("/degree-audit")
def degree_audit():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("degree_audit.html", user=user)


@app.route("/program-requirements")
def program_requirements():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("program_requirements.html", user=user)


@app.route("/apply-to-graduate")
def apply_to_graduate():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("apply_to_graduate.html", user=user)


@app.route("/scholarships")
def scholarships():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("scholarships.html", user=user)


@app.route("/financial-aid")
def financial_aid():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("financial_aid.html", user=user)


@app.route("/tuition-balance")
def tuition_balance():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("tuition_balance.html", user=user)


@app.route("/contact-advisor")
def contact_advisor():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("contact_advisor.html", user=user)


@app.route("/counseling-services")
def counseling_services():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("counseling_services.html", user=user)


@app.route("/it-help-desk")
def it_help_desk():
    user, redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return render_template("it_help_desk.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)