from music21 import stream, note, instrument, clef, environment # type:ignore
from music21.layout import StaffGroup
from PIL import Image, ImageOps #type:ignore
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
    

def invert_score_colors(path: Path) -> None:
    img = Image.open(path).convert('RGB')
    inverted = ImageOps.invert(img)
    inverted_path = path.with_name(path.stem + '_dark.png')
    inverted.save(inverted_path)


def clean_ly_file(path: str, staffsize=25) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned = [f"#(set-global-staff-size {staffsize})\n"]
    in_paper_block = False
    paper_modified = False

    #remove uncompatible lines and tagline
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

    # creates paper block if it doesn't exist
    if not paper_modified:
        cleaned.append("\n\\paper {\n  tagline = ##f\n}\n")

    with open(path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned)


def single_generate(measures):
    score = stream.Stream()

    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5']

    for _ in range(measures): # number of measures
        m = stream.Measure()
        for _ in range(4): # 4 notes each
            pitch = random.choice(notes)
            m.append(note.Note(pitch, quarterLength=1))
            
        score.append(m)
    return score


def duo_generate(measures):
    upper = stream.Part()
    upper.id = 'RH'
    upper.append(instrument.Piano())

    lower = stream.Part()
    lower.id = 'LH'
    lower.append(instrument.Piano())

    notes_treble = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5']
    notes_bass = ['E2', 'F2', 'G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F3']

    for i in range(measures):
        um = stream.Measure()
        lm = stream.Measure()

        if i == 0:
            um.insert(0, clef.TrebleClef())
            lm.insert(0, clef.BassClef())

        for _ in range(4):
            um.append(note.Note(random.choice(notes_treble), quarterLength=1))
            lm.append(note.Note(random.choice(notes_bass), quarterLength=1))

        upper.append(um)
        lower.append(lm)

    piano_group = StaffGroup([upper, lower], group='PianoStaff')
    piano_group.name = "Piano"

    score = stream.Score()

    score.append(upper)
    score.append(lower)
    return score


def generate_random_score(output_file='score', two_voices=False) -> None:

    # single voice
    if not two_voices:
        score = single_generate(40)

    # two voices
    else:
        score = duo_generate(30)

    ly_path = STATIC_DIR / f"{output_file}.ly"
    score.write('lilypond', fp=str(ly_path))

    clean_ly_file(ly_path)

    try:
        subprocess.run(['lilypond', "--png",  f'{output_file}.ly'], cwd=str(STATIC_DIR), check=True)
    except subprocess.CalledProcessError as e:
        print("STDERR:", e.stderr)
        raise RuntimeError(f"LilyPond failed: {e}") from e
    
    os.remove(ly_path)
    invert_score_colors(STATIC_DIR / f"{output_file}.png")