from flask import Blueprint, render_template
from utils.github import get_github_stars

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    stars = get_github_stars()
    return render_template("pages/landing.html", stars=stars)
