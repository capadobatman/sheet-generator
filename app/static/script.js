function applyTheme(theme) {
    const body = document.body;
    const image = document.getElementById("score");
    const normal = "/static/score.png";
    const dark = "/static/score_dark.png";

    if (theme === "dark") {
        body.classList.remove("bg-white");
        body.classList.add("bg-black");
        image.src = dark;
    } else {
        body.classList.remove("bg-black");
        body.classList.add("bg-white");
        image.src = normal;
    }
}

function toggleTheme() {
    const current = localStorage.getItem("theme");
    const next = current === "dark" ? "light" : "dark";
    localStorage.setItem("theme", next);
    applyTheme(next);
}

window.onload = () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    applyTheme(savedTheme);

    const savedOption = localStorage.getItem("chosenOption");
    if (savedOption) {
        const selectedInput = document.querySelector(`input[name="option"][value="${savedOption}"]`);
        if (selectedInput) selectedInput.checked = true;
    }

    const radioInputs = document.querySelectorAll('input[name="option"]');
    radioInputs.forEach((input) => {
        input.addEventListener("change", () => {
            if (input.checked) {
                localStorage.setItem("chosenOption", input.value);
            }
        });
    });
};