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
    if os.path.exists(IMAGE_PATH):
        os.remove(IMAGE_PATH)

    scale = request.form.get("scale")
    voice = request.form.get("num_voices")
    clef1 = request.form.get("clef1")
    min_note_1 = request.form.get("min_note_1")
    max_note_1 = request.form.get("max_note_1")

    if voice == "2":
        clef2 = request.form.get("clef2")
        min_note_2 = request.form.get("min_note_2")
        max_note_2 = request.form.get("max_note_2")
        generate_random_score(scale=scale, two_voices=True, notes1=[min_note_1, max_note_1], notes2=[min_note_2, max_note_2], clef1=clef1, clef2=clef2)

    else:
        generate_random_score(scale=scale, notes1=[min_note_1, max_note_1], clef1=clef1)

    return redirect(url_for('main.home'))