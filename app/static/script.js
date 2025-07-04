function applyTheme(theme) {
    const body = document.body;
    const lcolumn = document.getElementById("lcolumn");
    const image = document.getElementById("score");
    const normal = "/static/score.png";
    const dark = "/static/score_dark.png";

    if (theme === "dark") {
        body.classList.remove("bg-white");
        body.classList.add("bg-black");
        lcolumn.classList.remove("text-black");
        lcolumn.classList.add("text-white");
        image.src = dark;
    } else {
        body.classList.remove("bg-black");
        body.classList.add("bg-white");
        lcolumn.classList.remove("text-white");
        lcolumn.classList.add("text-black");
        image.src = normal;
    }
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