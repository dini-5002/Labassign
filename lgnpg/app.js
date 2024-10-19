document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('registerForm').addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent form from submitting

      // Get the values of the input fields
      let userID = document.getElementById('userid').value;
      let password = document.getElementById('password').value;
      let confirmPassword = document.getElementById('confirmPassword').value;
      let message = document.getElementById('message');

      // Clear any previous messages
      message.textContent = '';

      // Simple validation
      if (password !== confirmPassword) {
          message.textContent = 'Passwords do not match!';
          message.style.color = 'red'; // Show error in red
          return;
      }

      // If passwords match, show success message
      message.style.color = 'green';
      message.textContent = 'Registration successful!';

      // Clear the form after successful submission (optional)
      document.getElementById('registerForm').reset();
  });
});
