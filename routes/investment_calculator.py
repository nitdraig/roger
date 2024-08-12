from flask import Blueprint, render_template, request

investment_calculator_bp = Blueprint("investment_calculator", __name__)


@investment_calculator_bp.route("/investment-calculator", methods=["GET", "POST"])
def investment_calculator():
    if request.method == "POST":
        initial_investment = float(request.form.get("initial-investment"))
        interest_rate = float(request.form.get("interest-rate")) / 100
        years = int(request.form.get("years"))

        future_value = initial_investment * (1 + interest_rate) ** years

        return render_template(
            "pages/investment_calculator.html", future_value=future_value
        )

    return render_template("pages/investment_calculator.html")
