import os
from flask import Blueprint, render_template, redirect, url_for, request # type: ignore
from app.generator import generate_random_score
from pathlib import Path

main_bp = Blueprint('main', __name__)

BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "static" / "score.png"


@main_bp.route('/')
def home():
    if os.path.exists(IMAGE_PATH):
        return render_template('home.html')
    else:
        return render_template('home.html')



@main_bp.route('/generate', methods=["POST"])
def generate():
    option = request.form.get("num_voices")
    if os.path.exists(IMAGE_PATH):
        os.remove(IMAGE_PATH)

    if option == "2":
        generate_random_score(two_voices=True)

    else:
        generate_random_score()

    return redirect(url_for('main.home'))