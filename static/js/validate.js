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
        let raw = this.value.toUpperCase().replace(/[^A-Z0-9]/g, ''); // allow only A-Z, 0-9
        let formatted = '';

        // Enforce first 5 letters
        for (let i = 0; i < raw.length && i < 5; i++) {
            if (/[A-Z]/.test(raw[i])) {
                formatted += raw[i];
            }
        }

        // Enforce next 4 digits
        for (let i = 5; i < raw.length && formatted.length < 9; i++) {
            if (/[0-9]/.test(raw[i])) {
                formatted += raw[i];
            }
        }

        // Enforce final character (letter)
        for (let i = 9; i < raw.length && formatted.length < 10; i++) {
            if (/[A-Z]/.test(raw[i])) {
                formatted += raw[i];
            }
        }

        this.value = formatted;

        // Final validation only when length is 10
        const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]$/;
        if (formatted.length === 10 && !panPattern.test(formatted)) {
            this.setCustomValidity('PAN must be 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)');
        } else {
            this.setCustomValidity('');
        }
    });

    // Optional: block invalid keypresses
    panInput.addEventListener('keypress', function (e) {
        const char = e.key.toUpperCase();
        const value = panInput.value.toUpperCase();

        if (value.length >= 10) {
            e.preventDefault();
        } else if (value.length < 5 && !/[A-Z]/.test(char)) {
            e.preventDefault(); // Only letters for first 5
        } else if (value.length >= 5 && value.length < 9 && !/[0-9]/.test(char)) {
            e.preventDefault(); // Only digits for next 4
        } else if (value.length === 9 && !/[A-Z]/.test(char)) {
            e.preventDefault(); // Only letter for 10th character
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
