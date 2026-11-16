const sectionToggles = document.querySelectorAll(".section-toggle");

for (const toggle of sectionToggles) {
  const contentId = toggle.getAttribute("aria-controls");
  const content = contentId ? document.getElementById(contentId) : null;

  if (!content) continue;

  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    content.hidden = expanded;
  });
}
