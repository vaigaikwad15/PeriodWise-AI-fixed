"""PeriodWise AI Flask application."""

import os
from datetime import date, timedelta

from flask import Flask, render_template, session, redirect, url_for

from config.settings import SECRET_KEY, DEBUG, HOST, PORT
from models.cycle_model import get_cycles_by_user
from AI.cycle_predictor import predict_next_period


app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static",
    template_folder="templates"
)

app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)


# Authentication blueprint
from routes.routes_auth import auth_bp
app.register_blueprint(auth_bp)


# Application feature blueprints
from routes.cycle_routes import cycle_bp
from routes.symptom_routes import symptom_bp
from routes.wellness_routes import wellness_bp
from routes.analytics_routes import analytics_bp
from routes.profile_routes import profile_bp
from routes.reminder_routes import reminder_bp

app.register_blueprint(cycle_bp)
app.register_blueprint(symptom_bp)
app.register_blueprint(wellness_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reminder_bp)


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/service-worker.js")
def service_worker():
    response = app.send_static_file("service-worker.js")

    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Content-Type"] = "application/javascript"

    return response


@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name", "there")
    )


@app.route("/calendar")
def calendar():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = str(session["user_id"])

    cycles = get_cycles_by_user(user_id)

    calendar_periods = []

    for cycle in cycles:
        start_date = cycle.get("period_start_date")
        end_date = cycle.get("period_end_date")

        if start_date:
            calendar_periods.append({
                "start_date": str(start_date)[:10],
                "end_date": str(end_date or start_date)[:10]
            })

    # Prepare period start dates for prediction
    period_start_dates = []

    for cycle in cycles:
        start_date = cycle.get("period_start_date")

        if start_date:
            period_start_dates.append(str(start_date)[:10])

    # Predict next period
    prediction = predict_next_period(period_start_dates)

    estimated_period_dates = []

    if prediction.get("success"):
        next_start = date.fromisoformat(
            prediction["estimated_next_period"]
        )

        for day in range(5):
            estimated_date = next_start + timedelta(days=day)

            estimated_period_dates.append(
                estimated_date.isoformat()
            )

    return render_template(
        "calendar.html",
        calendar_periods=calendar_periods,
        estimated_period_dates=estimated_period_dates
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "PeriodWise AI"
    }, 200


@app.route("/insights")
def insights():
    return render_template("insights.html")


if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )