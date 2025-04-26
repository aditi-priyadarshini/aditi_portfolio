  const menuBtn = document.getElementById("menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const closeBtn = document.getElementById("close-btn");
  const menuLinks = document.querySelectorAll(".menu-link");

  // Open/Close Menu on Menu Button
  menuBtn.addEventListener("click", () => {
    toggleMenu();
  });

  // Close Menu on Close Button
  closeBtn.addEventListener("click", () => {
    closeMenu();
  });

  // Close Menu when clicking any link
  menuLinks.forEach(link => {
    link.addEventListener("click", () => {
      closeMenu();
    });
  });

  // Also close when clicking outside
  document.addEventListener("click", function (e) {
    if (!mobileMenu.contains(e.target) && !menuBtn.contains(e.target)) {
      closeMenu();
    }
  });

  // Toggle Menu
  function toggleMenu() {
    if (mobileMenu.classList.contains("translate-x-full")) {
      mobileMenu.classList.remove("translate-x-full");
      mobileMenu.classList.add("translate-x-0");
    } else {
      mobileMenu.classList.remove("translate-x-0");
      mobileMenu.classList.add("translate-x-full");
    }
  }

  // Close Menu
  function closeMenu() {
    mobileMenu.classList.add("translate-x-full");
    mobileMenu.classList.remove("translate-x-0");
  }

