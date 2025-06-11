document.addEventListener('DOMContentLoaded', function () {
    // First and Last Name validation
    const nameInputs = [document.getElementById('inputFirstName'), document.getElementById('inputLastName')];
    nameInputs.forEach(input => {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^A-Za-z]/g, '');
        });
    });

    // Aadhaar validation
    const adharInput = document.getElementById('adhar');
    if (adharInput) {
        adharInput.addEventListener('input', function () {
            let digits = this.value.replace(/\D/g, '').slice(0, 12);
            let formatted = digits.replace(/(.{4})/g, '$1 ').trim();
            this.value = formatted;
            if (digits.length !== 12) {
                this.setCustomValidity('Aadhaar number must be exactly 12 digits');
            } else {
                this.setCustomValidity('');
            }
        });
        adharInput.addEventListener('keypress', function (e) {
            if (!/\d/.test(e.key)) {
                e.preventDefault();
            }
        });
    }

    // PAN validation
    const panInput = document.getElementById('pan');
    if (panInput) {
        panInput.setAttribute('maxlength', '10');
        panInput.addEventListener('input', function () {
            this.value = this.value.replace(/[^A-Za-z0-9]/g, '').slice(0, 10).toUpperCase();
            if (this.value.length !== 10) {
                this.setCustomValidity('Please enter valid PAN Number');
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // Password show/hide toggle
    document.querySelectorAll('.toggle-password').forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.querySelector('i').classList.remove('fa-eye');
                this.querySelector('i').classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                this.querySelector('i').classList.remove('fa-eye-slash');
                this.querySelector('i').classList.add('fa-eye');
            }
        });
    });

    // Dropdowns: show selected value in field box
    const dropdowns = [
        { selectId: 'gender', displayId: 'gender_display' },
        { selectId: 'designation', displayId: 'designation_display' },
        { selectId: 'Reference_agent', displayId: 'Reference_agent_display' },
        { selectId: 'Agent_team', displayId: 'Agent_team_display' }
    ];
    dropdowns.forEach(function(drop) {
        const select = document.getElementById(drop.selectId);
        const display = document.getElementById(drop.displayId);
        if (select && display) {
            select.addEventListener('change', function () {
                display.value = select.value;
            });
        }
    });

    // Blur validation for all inputs/selects
    document.querySelectorAll('form input, form select').forEach(function (el) {
        el.addEventListener('blur', function () {
            if (el.checkValidity()) {
                el.classList.remove('is-invalid');
                el.classList.add('is-valid');
            } else {
                el.classList.remove('is-valid');
                el.classList.add('is-invalid');
            }
        });
    });

    // Password validation
    const passwordInput = document.getElementById("inputPassword");
    const confirmPasswordInput = document.getElementById("inputConfirmPassword");
    const confirmPasswordError = document.getElementById("confirmPasswordError");

    // Add ✅ spans next to password fields
    function createTick(input) {
        const span = document.createElement("span");
        span.textContent = " ✅";
        span.style.color = "green";
        span.style.fontWeight = "bold";
        span.style.display = "none";
        input.parentNode.appendChild(span);
        return span;
    }
    const passwordTick = createTick(passwordInput);
    const confirmTick = createTick(confirmPasswordInput);

    function validatePasswords() {
        const pwd = passwordInput.value;
        const cpwd = confirmPasswordInput.value;

        if (pwd === cpwd && pwd.length > 0) {
            confirmPasswordError.style.display = "none";
            passwordInput.style.border = "2px solid green";
            confirmPasswordInput.style.border = "2px solid green";
            passwordTick.style.display = "inline";
            confirmTick.style.display = "inline";
            return true;
        } else {
            confirmPasswordError.style.display = "block";
            confirmPasswordError.textContent = " Passwords do not match!";
            passwordInput.style.border = "2px solid red";
            confirmPasswordInput.style.border = "2px solid red";
            passwordTick.style.display = "none";
            confirmTick.style.display = "none";
            return false;
        }
    }

    passwordInput.addEventListener("input", validatePasswords);
    confirmPasswordInput.addEventListener("input", validatePasswords);

    // Form submit validation
    const form = document.querySelector("form");
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const pwdMatch = validatePasswords();

        if (!passwordInput.checkValidity()) {
            alert("Password does not meet the required complexity.");
            return;
        }

        if (!pwdMatch) {
            confirmPasswordInput.focus();
            return;
        }

        // Dropdowns required check
        let valid = true;
        dropdowns.forEach(drop => {
            const select = document.getElementById(drop.selectId);
            if (select && !select.value) {
                select.classList.add('is-invalid');
                valid = false;
            } else if (select) {
                select.classList.remove('is-invalid');
            }
        });

        if (!valid) {
            return;
        }
    });
});
