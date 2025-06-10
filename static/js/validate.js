// Validate on blur for all inputs/selects in the form
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('form input, form select').forEach(function(el) {
        el.addEventListener('blur', function() {
            if (el.checkValidity()) {
                el.classList.remove('is-invalid');
                el.classList.add('is-valid');
            } else {
                el.classList.remove('is-valid');
                el.classList.add('is-invalid');
            }
        });
    });

    // Login form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            let valid = true;
            const emailInput = loginForm.querySelector('#inputEmailAddress');
            const emailError = loginForm.querySelector('#emailError');
            const email = emailInput.value.trim();
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!email || !emailPattern.test(email)) {
                emailError.style.display = 'block';
                emailInput.classList.add('is-invalid');
                valid = false;
            } else {
                emailError.style.display = 'none';
                emailInput.classList.remove('is-invalid');
            }

            const passwordInput = loginForm.querySelector('#inputPassword');
            const passwordError = loginForm.querySelector('#passwordError');
            const password = passwordInput.value;
            const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,32}$/;
            if (!password || !passwordPattern.test(password)) {
                passwordError.style.display = 'block';
                passwordInput.classList.add('is-invalid');
                valid = false;
            } else {
                passwordError.style.display = 'none';
                passwordInput.classList.remove('is-invalid');
            }

            if (!valid) {
                e.preventDefault();
            }
            this.classList.add('was-validated');
        });
    }

    // Reset password form validation and confirmation message
    const resetForm = document.getElementById('resetForm');
    if (resetForm) {
        resetForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = resetForm.querySelector('#inputEmailAddress');
            const emailError = resetForm.querySelector('#emailError');
            const email = emailInput.value.trim();
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!email || !emailPattern.test(email)) {
                emailError.style.display = 'block';
                emailInput.classList.add('is-invalid');
            } else {
                emailError.style.display = 'none';
                emailInput.classList.remove('is-invalid');
                resetForm.style.display = 'none';
                const msg = document.createElement('div');
                msg.className = 'alert alert-success mt-3';
                msg.innerHTML = `A password reset link has been sent to <strong>${email}</strong>. Please check your email.`;
                resetForm.parentNode.insertBefore(msg, resetForm.nextSibling);
            }
            this.classList.add('was-validated');
        });
    }

    // Generic form validation for other forms
    document.querySelectorAll('form').forEach(function(form) {
        if (form !== loginForm && form !== resetForm) {
            form.addEventListener('submit', function(event) {
                if (!this.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                this.classList.add('was-validated');
            });
        }
    });
});