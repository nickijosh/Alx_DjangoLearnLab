// script.js - Basic JS for Django Blog

document.addEventListener("DOMContentLoaded", function () {
    console.log("Django Blog JavaScript loaded successfully!");

    // Example: Alert when a button is clicked
    const alertButtons = document.querySelectorAll(".btn-alert");
    alertButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            alert("Button clicked!");
        });
    });
});
