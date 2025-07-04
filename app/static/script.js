function applyTheme(theme) {
    const body = document.body;
    const lcolumn = document.getElementById("lcolumn");
    const image = document.getElementById("score");
    const selects = [
        document.getElementById("select1l"),
        document.getElementById("select1h"),
        document.getElementById("select2l"),
        document.getElementById("select2h")
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

window.onload = () => {
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