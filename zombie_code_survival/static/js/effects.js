document.addEventListener("DOMContentLoaded", function () {
  // Terminal typing effect for narrative elements
  const typewriterElements = document.querySelectorAll(".typewriter");
  typewriterElements.forEach((el) => {
    const text = el.textContent;
    el.textContent = "";
    let i = 0;
    const timer = setInterval(() => {
      if (i < text.length) {
        el.textContent += text.charAt(i);
        i++;
      } else {
        clearInterval(timer);
        el.style.borderRight = "none";
      }
    }, 50);
  });

  // Random glitch effects
  setInterval(() => {
    if (Math.random() > 0.7) {
      const glitch = document.createElement("div");
      glitch.style.position = "fixed";
      glitch.style.top = Math.random() * 100 + "vh";
      glitch.style.left = Math.random() * 100 + "vw";
      glitch.style.width = Math.random() * 100 + 50 + "px";
      glitch.style.height = "2px";
      glitch.style.background = "rgba(255, 0, 0, 0.5)";
      glitch.style.zIndex = "1000";
      glitch.style.pointerEvents = "none";
      document.body.appendChild(glitch);

      setTimeout(() => {
        document.body.removeChild(glitch);
      }, 100);
    }
  }, 3000);

  // Terminal cursor effect for code editor
  const codeEditor = document.querySelector(".code-editor");
  if (codeEditor) {
    codeEditor.addEventListener("focus", function () {
      this.style.caretColor = "var(--main-text-color)";
    });

    codeEditor.addEventListener("blur", function () {
      this.style.caretColor = "transparent";
    });
  }

  // Hazard icon animation
  const hazardIcons = document.querySelectorAll(".hazard-icon");
  hazardIcons.forEach((icon) => {
    setInterval(() => {
      icon.style.opacity = Math.random() > 0.5 ? 1 : 0.7;
    }, 1000);
  });
});
