import os
from flask import Blueprint, render_template, request, send_file
from app.generator import generate_random_score

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filename = 'random_score'  # Pode ser dinâmico se quiser
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        output_path = os.path.join(base_dir, 'outputs', f'{filename}.pdf')

        generate_random_score(output_file=filename)

        if not os.path.exists(output_path):
            return "File not found", 404

        return send_file(output_path, as_attachment=True)

    return render_template('index.html')
