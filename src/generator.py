from music21 import stream, note, meter, key, environment # type: ignore
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

def generate_random_score(output_file='outputs/random_score'):
    configure_lilypond()

    s = stream.Stream()
    s.append(meter.TimeSignature("4/4"))
    s.append(key.KeySignature(0))  # C major

    notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
    for _ in range(4):  # 4 measures
        for _ in range(4):  # 4 quarter notes
            pitch = random.choice(notes)
            s.append(note.Note(pitch, quarterLength=1))

    s.includeLayout = False
    s.write('lilypond', fp=f'{output_file}.ly') 

    try:
        subprocess.run(['lilypond', f'{output_file}.ly'], check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError(f"LilyPond failed to compile {output_file}.ly")
