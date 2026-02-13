document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("lead-form");
    const submitBtn = document.getElementById("submit-btn");
  
    if (form && submitBtn) {
      form.addEventListener("submit", () => {
        submitBtn.disabled = true;
        submitBtn.textContent = "Submitting...";
      });
    }
  });