"""
PeriodWise AI - Cycle Predictor

This module estimates the next period start date
using the user's previous period start dates.
"""

from datetime import date, datetime
from statistics import median


def predict_next_period(period_dates):
    """
    Estimate the next period start date.

    Parameters:
        period_dates (list):
            Previous period start dates in YYYY-MM-DD format.

    Returns:
        dict:
            Estimated next period date and cycle information.
    """

    if not period_dates or len(period_dates) < 2:
        return {
            "success": False,
            "message": (
                "At least two period start dates are needed "
                "to estimate your next period."
            )
        }

    try:
        dates = []

        for period_date in period_dates:

            if isinstance(period_date, datetime):
                parsed_date = period_date.date()

            elif isinstance(period_date, date):
                parsed_date = period_date

            else:
                parsed_date = datetime.strptime(
                    period_date,
                    "%Y-%m-%d"
                ).date()

            dates.append(parsed_date)

        dates.sort()

    except (ValueError, TypeError):
        return {
            "success": False,
            "message": (
                "Invalid date format. "
                "Please use YYYY-MM-DD."
            )
        }

    # Remove duplicate dates.
    unique_dates = sorted(set(dates))

    if len(unique_dates) < 2:
        return {
            "success": False,
            "message": (
                "Two different period start dates are required."
            )
        }

    # Calculate intervals between consecutive period starts.
    cycle_lengths = []

    for index in range(1, len(unique_dates)):

        cycle_length = (
            unique_dates[index] - unique_dates[index - 1]
        ).days

        # Ignore implausible intervals rather than using them.
        if 15 <= cycle_length <= 60:
            cycle_lengths.append(cycle_length)

    if not cycle_lengths:
        return {
            "success": False,
            "message": (
                "There is not enough valid cycle history "
                "to estimate the next period."
            )
        }

    # Use the median to reduce the influence of unusual cycles.
    average_cycle_length = round(median(cycle_lengths))

    last_period_start = unique_dates[-1]

    estimated_next_period = (
        last_period_start.fromordinal(
            last_period_start.toordinal() + average_cycle_length
        )
    )

    return {
        "success": True,
        "last_period_start": last_period_start.isoformat(),
        "cycle_lengths": cycle_lengths,
        "estimated_cycle_length": average_cycle_length,
        "estimated_next_period": estimated_next_period.isoformat(),
        "message": (
            "This is an estimate, not a guaranteed date. "
            "Menstrual cycles can naturally vary."
        )
    }