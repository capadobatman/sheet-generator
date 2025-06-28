function setTheme(isDark) {
  const body = document.body;
  const img = document.getElementById("scoreImage");
  const buttons = [document.getElementById("generateBtn"), document.getElementById("themeToggleBtn")];

  if (isDark) {
    body.style.backgroundColor = "black";
    body.style.color = "white";
    if (img) img.src = "/static/score_dark.png";
    localStorage.setItem('theme', 'dark');
    buttons.forEach(btn => {
      if (btn) {
        btn.classList.remove('light');
        btn.classList.add('dark');
      }
    });
  } else {
    body.style.backgroundColor = "white";
    body.style.color = "black";
    if (img) img.src = "/static/score.png";
    localStorage.setItem('theme', 'light');
    buttons.forEach(btn => {
      if (btn) {
        btn.classList.remove('dark');
        btn.classList.add('light');
      }
    });
  }
}

function toggleTheme() {
  const current = localStorage.getItem('theme');
  setTheme(current !== 'dark');
}

window.onload = function () {
  const saved = localStorage.getItem('theme');
  setTheme(saved === 'dark');
};
