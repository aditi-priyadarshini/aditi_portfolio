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

//contact page 
  document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = {
      name: document.getElementById('name').value,
      email: document.getElementById('email').value,
      phone: document.getElementById('phone').value,
      subject: document.getElementById('subject').value,
      message: document.getElementById('message').value,
      time: new Date().toLocaleString(),
    };

    emailjs.send('service_3cvi0qu', 'template_vei2793', formData)
    .then(function(response) {
      console.log('SUCCESS!', response.status, response.text);

      // Show success message
      const successMsg = document.getElementById('success-message');
      successMsg.classList.remove('hidden');
      successMsg.classList.add('block');

      // Hide it after 3 seconds
      setTimeout(() => {
        successMsg.classList.remove('block');
        successMsg.classList.add('hidden');
      }, 3000);

      // Clear form
      document.getElementById('contact-form').reset();

    }, function(error) {
      console.error('FAILED...', error);
      alert('❌ Failed to send message. Try again.');
    });
});
