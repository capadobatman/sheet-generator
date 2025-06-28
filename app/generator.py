from music21 import stream, note, meter, key, environment # type:ignore
import random
import os
import shutil
import subprocess
from pathlib import Path


STATIC_DIR = Path(__file__).resolve().parent / "static"
STATIC_DIR.mkdir(exist_ok=True)


def configure_lilypond() -> None:
    lily_path = shutil.which("lilypond")
    if lily_path:
        env = environment.UserSettings()
        env['lilypondPath'] = lily_path
    else:
        raise EnvironmentError("LilyPond not found in PATH.")


def clean_ly_file(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned = []
    in_paper_block = False
    paper_modified = False

    #remove uncompatible lines andd tagline
    for line in lines:
        if "lilypond-book-preamble.ly" in line:
            continue

        if "RemoveEmptyStaffContext" in line or "VerticalAxisGroup" in line:
            continue

        if "\\paper" in line:
            in_paper_block = True

        if in_paper_block and "}" in line and not paper_modified:
            cleaned.append("  tagline = ##f\n")  
            paper_modified = True
            in_paper_block = False

        cleaned.append(line)

    if not paper_modified:
        cleaned.append("\n\\paper {\n  tagline = ##f\n}\n")

    with open(path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned)


def generate_random_score(output_file='score') -> None:

    s = stream.Stream()
    s.append(meter.TimeSignature("4/4"))
    s.append(key.KeySignature(0))

    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']

    for _ in range(40): # 40 measures
        m = stream.Measure()
        for _ in range(4): # 4 notes each
            pitch = random.choice(notes)
            m.append(note.Note(pitch, quarterLength=1))
            
        s.append(m)

    ly_path = STATIC_DIR / f"{output_file}.ly"
    s.write('lilypond', fp=str(ly_path))

    clean_ly_file(ly_path)

    try:
        subprocess.run(['lilypond', "--png",  f'{output_file}.ly'], cwd=str(STATIC_DIR), check=True)
    except subprocess.CalledProcessError as e:
        print("STDERR:", e.stderr)
        raise RuntimeError(f"LilyPond failed: {e}") from e
    
    os.remove(ly_path)