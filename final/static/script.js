document.addEventListener("DOMContentLoaded", () => {
    const userIcon = document.querySelector('.user-icon');
    const dropdown = document.getElementById('userDropdown');
  
    // Toggle dropdown visibility on user icon click
    userIcon.addEventListener("click", (e) => {
        e.stopPropagation(); // Prevent click from bubbling to document
        dropdown.classList.toggle("show");
    });
  });
  // Close dropdown if clicked outside
  window.addEventListener("click", (e) => {
      if (!userIcon.contains(e.target) && !dropdown.contains(e.target)) {
          dropdown.classList.remove("show");
      }
  });
  
  document.getElementById("logoutLink").addEventListener("click", async function (e) {
    e.preventDefault();
  
    try {
        const response = await fetch("http://127.0.0.1:5006/logout", {
            method: "POST"
        });
  
        if (response.ok) {
            window.location.href = "http://127.0.0.1:5500/login/login.html"; // Redirect to login (5002)
        } else {
            alert("Logout failed.");
        }
    } catch (error) {
        console.error("Error logging out:", error);
        alert("Logout error");
    }
  });
  
  document.getElementById("DeleteLink").addEventListener("click", async function (e) {
    e.preventDefault();
  
    const confirmDelete = confirm("Are you sure you want to delete your account?");
    if (!confirmDelete) return;
  
    try {
        // Sending the POST request to delete the account
        const response = await fetch("http://127.0.0.1:5006/delete_account", {
            method: "POST"
        });
  
        if (response.ok) {
            alert("Account deleted successfully.");
            window.location.href = "http://127.0.0.1:5500/login/login.html";  // Redirect to login page after deletion (5002)
        } else {
            const data = await response.json();
            alert(data.error || "Account deletion failed.");
        }
    } catch (error) {
        console.error("Error deleting account:", error);
        alert("Error deleting account.");
    }
  });
  function redirectToPage(url) {
    window.location.href = url;
  }