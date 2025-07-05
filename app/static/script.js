const allNotes = [
  "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
  "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
  "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
  "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
  "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6"
];

function applyTheme(theme) {
    const body = document.body;
    const lcolumn = document.getElementById("lcolumn");
    const image = document.getElementById("score");
    const selects = [
        document.getElementById("select1l"),
        document.getElementById("select1h"),
        document.getElementById("select2l"),
        document.getElementById("select2h"),
        document.getElementById("selectclef1"),
        document.getElementById("selectclef2"),
        document.getElementById("scale")
    ];

    const isDark = theme === "dark";
    body.classList.toggle("bg-white", !isDark);
    body.classList.toggle("bg-black", isDark);
    lcolumn.classList.toggle("text-black", !isDark);
    lcolumn.classList.toggle("text-white", isDark);
    image.src = isDark ? "/static/score_dark.png" : "/static/score.png";

    selects.forEach(select => {
        select.classList.toggle("bg-white", !isDark);
        select.classList.toggle("bg-black", isDark);
    });
}

function toggleTheme() {
    const current = localStorage.getItem("theme");
    const next = current === "dark" ? "light" : "dark";
    localStorage.setItem("theme", next);
    applyTheme(next);
}

function toggleVoiceFields() {
  const isTwoVoices = document.querySelector('input[name="num_voices"][value="2"]').checked;
  const voice2 = document.getElementById("voice2");
  voice2.classList.toggle("hidden", !isTwoVoices);
}

const clefRangeMap = {
    T: { min: 4, max: 6 },
    A: { min: 3, max: 5 },
    B: { min: 2, max: 4 }
};

function populateNoteSelect(selectId, minOctave = 2, maxOctave = 6) {
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const select = document.getElementById(selectId);
    select.innerHTML = '';

    for (let octave = minOctave; octave <= maxOctave; octave++) {
        for (let note of notes) {
            const value = note + octave;
            const option = new Option(value, value);
            select.add(option);
        }
    }
}

function updateNoteSelects(clefSelectId, lowSelectId, highSelectId) {
    const clef = document.getElementById(clefSelectId).value;
    const range = clefRangeMap[clef] || { min: 2, max: 6 };
    populateNoteSelect(lowSelectId, range.min, range.max);
    populateNoteSelect(highSelectId, range.min, range.max);
}

function updateHighNoteOptions(lowSelectId, highSelectId, minSemitones = 3) {
    const lowValue = document.getElementById(lowSelectId).value;
    const highSelect = document.getElementById(highSelectId);
    
    const startIndex = allNotes.indexOf(lowValue);
    highSelect.innerHTML = ''; // limpa

    const options = allNotes.slice(startIndex + minSemitones);

    options.forEach(note => {
        const opt = new Option(note, note);
        highSelect.add(opt);
    });
}

const majorScales = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'];
const minorScales = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'];

function populateScaleSelect(selectId) {
    const select = document.getElementById(selectId);
    select.innerHTML = '';

    const groupMajor = document.createElement('optgroup');
    groupMajor.label = 'Major';
    majorScales.forEach(scale => {
        const option = new Option(scale + ' Major', scale + '_major');
        groupMajor.appendChild(option);
    });

    const groupMinor = document.createElement('optgroup');
    groupMinor.label = 'Minor';
    minorScales.forEach(scale => {
        const option = new Option(scale + ' Minor', scale + '_minor');
        groupMinor.appendChild(option);
    });

    select.appendChild(groupMajor);
    select.appendChild(groupMinor);
}

window.onload = () => {
    populateScaleSelect('scale');

    document.getElementById("selectclef1").addEventListener("change", () => {
        updateNoteSelects("selectclef1", "select1l", "select1h");
    });
    document.getElementById("selectclef2").addEventListener("change", () => {
        updateNoteSelects("selectclef2", "select2l", "select2h");
    });
    document.getElementById("select1l").addEventListener("change", () => {
    updateHighNoteOptions("select1l", "select1h");
    });

    document.getElementById("select2l").addEventListener("change", () => {
        updateHighNoteOptions("select2l", "select2h");
    });

    updateNoteSelects("selectclef1", "select1l", "select1h");
    updateNoteSelects("selectclef2", "select2l", "select2h");

    updateHighNoteOptions("select1l", "select1h");
    updateHighNoteOptions("select2l", "select2h");


    const savedTheme = localStorage.getItem("theme") || "light";
    applyTheme(savedTheme);

    const savedOption = localStorage.getItem("chosenOption");
    if (savedOption) {
        const selectedInput = document.querySelector(`input[name="num_voices"][value="${savedOption}"]`);
        if (selectedInput) selectedInput.checked = true;
    }

    const radioInputs = document.querySelectorAll('input[name="num_voices"]');
    radioInputs.forEach((input) => {
        input.addEventListener("change", () => {
            if (input.checked) {
                localStorage.setItem("chosenOption", input.value);
            }
        });
    });

    toggleVoiceFields();
};
