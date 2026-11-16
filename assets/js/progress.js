const progressBar = document.querySelector(".reading-progress-bar");
const progressTrack = document.querySelector(".reading-progress");

if (progressBar && progressTrack) {
  let frameRequested = false;

  const updateProgress = () => {
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollableHeight > 0
      ? Math.min(1, Math.max(0, window.scrollY / scrollableHeight))
      : 0;

    progressBar.style.transform = `scaleX(${progress})`;
    progressTrack.setAttribute("aria-valuenow", String(Math.round(progress * 100)));
    frameRequested = false;
  };

  const scheduleUpdate = () => {
    if (frameRequested) return;
    frameRequested = true;
    window.requestAnimationFrame(updateProgress);
  };

  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", scheduleUpdate);
  updateProgress();
}
