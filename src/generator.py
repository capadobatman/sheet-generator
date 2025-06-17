from music21 import stream, note, meter, key, environment # type:ignore
import random
import os
import shutil
import subprocess


os.makedirs('outputs', exist_ok=True)


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
            continue  # Remove a linha
        cleaned.append(line)

    with open(path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned)

def generate_random_score(output_file='outputs/random_score'):
    configure_lilypond()

    s = stream.Stream()
    s.append(meter.TimeSignature("4/4"))
    s.append(key.KeySignature(0))  # C major

    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
    for _ in range(4):
        for _ in range(4):
            pitch = random.choice(notes)
            s.append(note.Note(pitch, quarterLength=1))

    ly_path = f'{output_file}.ly'
    s.write('lilypond', fp=ly_path)

    # Corrige o .ly antes de chamar o LilyPond
    clean_ly_file(ly_path)

    try:
        subprocess.run(['lilypond', ly_path], check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError(f"LilyPond failed to compile {ly_path}")
