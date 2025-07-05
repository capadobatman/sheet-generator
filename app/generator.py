from music21 import stream, note, instrument, clef, environment, scale, pitch, key # type:ignore
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


def single_generate(measures, notes, clef1, scale):
    score = stream.Stream()

    for i in range(measures): # number of measures
        m = stream.Measure()

        if i == 0:
            m.insert(0, clef_tl(clef1))
            score.insert(0, get_key_signature(scale))

        for _ in range(4): # 4 notes each
            pitch = random.choice(notes)
            m.append(note.Note(pitch, quarterLength=1))
            
        score.append(m)
    return score


def duo_generate(measures, notes1, notes2, clef1, clef2, scale):
    upper = stream.Part()
    upper.id = 'RH'
    upper.append(instrument.Piano())

    lower = stream.Part()
    lower.id = 'LH'
    lower.append(instrument.Piano())

    for i in range(measures):
        um = stream.Measure()
        lm = stream.Measure()

        if i == 0:
            um.insert(0, clef_tl(clef1))
            lm.insert(0, clef_tl(clef2))
            um.insert(0, get_key_signature(scale))

        for _ in range(4):
            um.append(note.Note(random.choice(notes1), quarterLength=1))
            lm.append(note.Note(random.choice(notes2), quarterLength=1))

        upper.append(um)
        lower.append(lm)

    piano_group = StaffGroup([upper, lower], group='PianoStaff')
    piano_group.name = "Piano"

    score = stream.Score()

    score.append(upper)
    score.append(lower)
    return score


def clef_tl(clef_: str):
    clef_map = {
        "T": clef.TrebleClef,
        "A": clef.AltoClef,
        "B": clef.BassClef
    }

    if clef_ not in clef_map:
        raise ValueError(f"Clef '{clef_}' not recognized.")

    return clef_map[clef_]()


def get_scale_notes(scale_name: str) -> list:
    tonic, mode = scale_name.split("_")
    if mode == "major":
        s = scale.MajorScale(tonic)
    
    else:
        s = scale.MinorScale(tonic)

    return [str(pitch) for pitch in s.getPitches('C2', 'B6')]


def get_key_signature(scale_name:str):
    tonic, mode = scale_name.split("_")
    k = key.Key(tonic, mode)
    return key.KeySignature(k.sharps)


def note_range(notes: list, scale: str) -> list:
    low_pitch, high_pitch = notes[0], notes[1]
    scale_range = get_scale_notes(scale)

    try:
        ind1 = scale_range.index(low_pitch)
        ind2 = scale_range.index(high_pitch) + 1
        return scale_range[ind1:ind2]
    
    except ValueError:
        low_midi = pitch.Pitch(low_pitch).midi
        high_midi = pitch.Pitch(high_pitch).midi

        filtered_range = []
        for note in scale_range:
            if low_midi <= pitch.Pitch(note).midi <= high_midi:
                filtered_range.append(note)

        return filtered_range


def generate_random_score(output_file='score', scale="C_major", two_voices=False, notes1=["C4", "B4"], notes2=["C3", "B3"], clef1="T", clef2="T") -> None:
    notes1 = note_range(notes=notes1, scale=scale)

    # single voice
    if not two_voices:
        score = single_generate(40, notes=notes1, clef1=clef1, scale=scale)

    # two voices
    else:
        notes2 = note_range(notes2, scale=scale)
        score = duo_generate(30, notes1=notes1, notes2=notes2, clef1=clef1, clef2=clef2, scale=scale)

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