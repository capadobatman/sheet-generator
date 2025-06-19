from music21 import stream, note, meter, key, environment # type:ignore
import random
import os
import shutil
import subprocess
from pathlib import Path


STATIC_DIR = Path(__file__).resolve().parent / "static"
STATIC_DIR.mkdir(exist_ok=True)


def configure_lilypond():
    lily_path = shutil.which("lilypond")
    if lily_path:
        env = environment.UserSettings()
        env['lilypondPath'] = lily_path
    else:
        raise EnvironmentError("LilyPond not found in PATH.")

def clean_ly_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned = []
    for line in lines:
        if "RemoveEmptyStaffContext" in line or "VerticalAxisGroup" in line:
            continue  
        cleaned.append(line)

    with open(path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned)

def generate_random_score(output_file='score'):

    s = stream.Stream()
    s.append(meter.TimeSignature("4/4"))
    s.append(key.KeySignature(0))  # C major

    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
    for _ in range(4):
        for _ in range(4):
            pitch = random.choice(notes)
            s.append(note.Note(pitch, quarterLength=1))

    ly_path = STATIC_DIR / f"{output_file}.ly"
    s.write('lilypond', fp=str(ly_path))

    clean_ly_file(ly_path)

    try:
        subprocess.run(['lilypond', "--png",  f'{output_file}.ly'], cwd=str(STATIC_DIR), check=True)
    except subprocess.CalledProcessError as e:
        print("STDERR:", e.stderr)
        raise RuntimeError(f"LilyPond failed: {e}") from e
    
    os.remove(ly_path)