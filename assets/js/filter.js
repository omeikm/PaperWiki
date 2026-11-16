const filterButtons = [...document.querySelectorAll("[data-filter]")];
const paperCards = [...document.querySelectorAll("[data-paper-card]")];
const emptyState = document.querySelector("[data-empty-state]");
const visibleCount = document.querySelector("#visible-count");

function showPapers(tag) {
  let shown = 0;

  for (const card of paperCards) {
    const tags = card.dataset.tags.split("|");
    const matches = tag === "all" || tags.includes(tag);
    card.hidden = !matches;
    if (matches) shown += 1;
  }

  if (emptyState) emptyState.hidden = shown !== 0;
  if (visibleCount) visibleCount.textContent = String(shown);
}

for (const button of filterButtons) {
  button.addEventListener("click", () => {
    for (const item of filterButtons) {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    }

    showPapers(button.dataset.filter);
  });
}
