"""
PeriodWise AI - Authentication Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from services.user_service import (
    register_user,
    authenticate_user
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get(
            "confirm_password", ""
        )

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        result = register_user(
            name=name,
            email=email,
            password=password
        )

        if result.get("success"):
            flash(
                "Registration successful. Please log in.",
                "success"
            )
            return redirect(url_for("auth.login"))

        flash(
            result.get("message", "Registration failed."),
            "danger"
        )

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        result = authenticate_user(email, password)

        if result.get("success"):

            user = result["user"]

            # Prevent session fixation.
            session.clear()

            session["user_id"] = user["_id"]
            session["user_name"] = user.get("name", "")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))