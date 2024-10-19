document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Get the values of the input fields
        let userID = document.getElementById('userid').value;
        let mobileNumber = document.getElementById('mobile_number').value;
        let password = document.getElementById('password').value;
        let confirmPassword = document.getElementById('confirmPassword').value;
        let message = document.getElementById('message');

        // Clear any previous messages
        message.textContent = '';

        // Simple validation
        if (!userID || !mobileNumber || !password || !confirmPassword) {
            message.textContent = 'All fields are required!';
            message.style.color = 'red';
            return;
        }

        if (password !== confirmPassword) {
            message.textContent = 'Passwords do not match!';
            message.style.color = 'red';
            return;
        }
        message.style.color = 'green';
        message.textContent = 'Registration successful!';
        // If validations pass, submit the form
        this.submit();  // Allows the form to be submitted to the server after validation
    });
});
