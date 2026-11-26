(() => {
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => {}));
  }
  document.querySelectorAll(".faq-list details").forEach(item => {
    item.addEventListener("toggle", () => {
      if (!item.open) return;
      document.querySelectorAll(".faq-list details").forEach(other => {
        if (other !== item) other.open = false;
      });
    });
  });
})();
