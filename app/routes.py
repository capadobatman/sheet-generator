import os
from flask import Blueprint, render_template, redirect, url_for
from app.generator import generate_random_score
from pathlib import Path

main_bp = Blueprint('main', __name__)

BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "static" / "score.png"


@main_bp.route('/')
def index():
    if os.path.exists(IMAGE_PATH):
        return render_template('index.html', image=IMAGE_PATH)
    else:
        return render_template('index.html', image=None)


@main_bp.route('/generate')
def generate():
    if os.path.exists(IMAGE_PATH):
        os.remove(IMAGE_PATH)

    generate_random_score()

    return redirect(url_for('main.index'))