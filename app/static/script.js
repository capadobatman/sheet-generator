function applyTheme(theme) {
    const body = document.body;
    const toggleBtn = document.getElementById("botao");
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
    const saved = localStorage.getItem("theme") || "light";
    applyTheme(saved);
};
