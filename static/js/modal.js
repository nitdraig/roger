// modal.js

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('disclaimer-modal');
    const openModalButton = document.getElementById('open-disclaimer');
    const closeModalButton = document.getElementById('close-modal');
  
    // Function to open the modal
    function openModal() {
      modal.style.display = 'block';
    }
  
    // Function to close the modal
    function closeModal() {
      modal.style.display = 'none';
    }
  
    // Event listeners
    if (openModalButton) {
      openModalButton.addEventListener('click', openModal);
    }
  
    if (closeModalButton) {
      closeModalButton.addEventListener('click', closeModal);
    }
  
    // Close the modal if the user clicks outside of it
    window.addEventListener('click', (event) => {
      if (event.target === modal) {
        closeModal();
      }
    });
  });
  