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


@app.route("/")
def home():
    user = get_logged_in_user()

    if not user:
        return redirect(url_for("login"))

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
    user = get_logged_in_user()

    if not user:
        return redirect(url_for("login"))

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


if __name__ == "__main__":
    app.run(debug=True)