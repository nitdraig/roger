document.addEventListener("DOMContentLoaded", () => {
  const sharpeRatioModal = document.getElementById("sharpe-ratio-modal");
  const openSharpeRatioButton = document.getElementById("open-sharpe-ratio");
  const closeSharpeRatioButton = document.getElementById("close-sharpe-ratio");

  function openModal() {
    sharpeRatioModal.style.display = "block";
  }

  function closeModal() {
    sharpeRatioModal.style.display = "none";
  }

  if (openSharpeRatioButton) {
    openSharpeRatioButton.addEventListener("click", openModal);
  }

  if (closeSharpeRatioButton) {
    closeSharpeRatioButton.addEventListener("click", closeModal);
  }

  window.addEventListener("click", (event) => {
    if (event.target === sharpeRatioModal) {
      closeModal();
    }
  });
});
