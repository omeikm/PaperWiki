const moodButton = document.querySelector("[data-mood-badge]");

if (moodButton) {
  const moods = ["🌱 初讀萌芽", "☕ 深度消化中", "💡 靈感爆發", "🤯 看到懷疑人生"];
  const paperId = moodButton.dataset.paperId;
  const storageKey = `paperwiki:mood:${paperId}`;
  const savedMood = Number(window.localStorage.getItem(storageKey));
  let moodIndex = Number.isInteger(savedMood) && savedMood >= 0 && savedMood < moods.length
    ? savedMood
    : 0;

  const renderMood = () => {
    moodButton.textContent = moods[moodIndex];
    moodButton.setAttribute("aria-label", `閱讀狀態：${moods[moodIndex]}。點擊切換狀態`);
    moodButton.title = "點擊切換閱讀狀態";
  };

  renderMood();
  moodButton.addEventListener("click", () => {
    moodIndex = (moodIndex + 1) % moods.length;
    window.localStorage.setItem(storageKey, String(moodIndex));
    renderMood();
  });
}
