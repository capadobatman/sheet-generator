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

window.onload = () => {
    updateNoteSelects("selectclef1", "select1l", "select1h");
    updateNoteSelects("selectclef2", "select2l", "select2h");

    document.getElementById("selectclef1").addEventListener("change", () => {
        updateNoteSelects("selectclef1", "select1l", "select1h");
    });
    document.getElementById("selectclef2").addEventListener("change", () => {
        updateNoteSelects("selectclef2", "select2l", "select2h");
    });

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
