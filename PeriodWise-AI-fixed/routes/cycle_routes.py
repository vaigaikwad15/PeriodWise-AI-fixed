"""
PeriodWise AI - Cycle Routes
"""

from datetime import date

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from routes import login_required

from models.cycle_model import (
    add_cycle,
    get_cycles_by_user,
    get_latest_cycle
)

from AI.cycle_predictor import predict_next_period


cycle_bp = Blueprint("cycle", __name__)


@cycle_bp.route("/cycle", methods=["GET", "POST"])
@login_required
def cycle_page():

    user_id = str(session["user_id"])

    if request.method == "POST":

        start_date = request.form.get(
            "period_start_date", ""
        ).strip()

        end_date = request.form.get(
            "period_end_date", ""
        ).strip()

        result = add_cycle(
            user_id=user_id,
            period_start_date=start_date,
            period_end_date=end_date or None
        )

        if result.get("success"):
            flash(
                "Period record saved successfully.",
                "success"
            )
        else:
            flash(
                result.get("message", "Unable to save record."),
                "danger"
            )

        return redirect(url_for("cycle.cycle_page"))

    # Get all cycle records
    cycles = get_cycles_by_user(user_id)

    # Calculate cycle length
    for index, cycle in enumerate(cycles):

        if index + 1 < len(cycles):

            current_date = date.fromisoformat(
                cycle["period_start_date"]
            )

            next_date = date.fromisoformat(
                cycles[index + 1]["period_start_date"]
            )

            cycle["cycle_length"] = (
                next_date - current_date
            ).days

        else:
            cycle["cycle_length"] = None

    # Get latest cycle
    latest_cycle = get_latest_cycle(user_id)

    # Predict next period
    prediction = predict_next_period([
        cycle["period_start_date"]
        for cycle in cycles
    ])

    return render_template(
        "cycle.html",
        cycles=cycles,
        latest_cycle=latest_cycle,
        prediction=prediction
    )