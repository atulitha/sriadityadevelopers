
document.addEventListener('DOMContentLoaded', function () {
    // First and Last Name validation
    const nameInputs = [document.getElementById('inputFirstName'), document.getElementById('inputLastName')];
    nameInputs.forEach(input => {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^A-Za-z]/g, '');
        });
    });

    // Aadhaar validation
    const aadhaarInput = document.getElementById('adhar');
    aadhaarInput.setAttribute('maxlength', '12');
    aadhaarInput.addEventListener('input', function () {
        this.value = this.value.replace(/\D/g, '').slice(0, 12);
    });

    // PAN validation
    const panInput = document.getElementById('pan');
    if (panInput) {
        panInput.setAttribute('maxlength', '10');
        panInput.addEventListener('input', function () {
            this.value = this.value.replace(/[^A-Za-z0-9]/g, '').slice(0, 10);
        });
    }

    // Password match validation
    const password = document.getElementById('inputPassword');
    const confirmPassword = document.getElementById('inputConfirmPassword');
    const confirmPasswordError = document .getElementById('confirmPasswordError');
    function checkPasswordMatch() {
        if (password.value !== confirmPassword.value) {
            confirmPasswordError.style.display = 'block';
            confirmPasswordError.textContent = 'Passwords do not match';
            confirmPassword.setCustomValidity('Passwords do not match');
        } else {
            confirmPasswordError.style.display = 'none';
            confirmPassword.setCustomValidity('');
        }
    }
    password.addEventListener('input', checkPasswordMatch);
    confirmPassword.addEventListener('input', checkPasswordMatch);

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

    // Form submit validation
    const form = document.querySelector('form');
    form.addEventListener('submit', function (e) {
        let valid = true;
        // Check dropdowns
        dropdowns.forEach(drop => {
            const select = document.getElementById(drop.id);
            if (select && !select.value) {
                select.classList.add('is-invalid');
                valid = false;
            } else if (select) {
                select.classList.remove('is-invalid');
            }
        });
        // Aadhaar length
        if (aadhaarInput.value.length !== 12) {
            aadhaarInput.classList.add('is-invalid');
            valid = false;
        } else {
            aadhaarInput.classList.remove('is-invalid');
        }
        // PAN length
        if (panInput && panInput.value.length !== 10) {
            panInput.classList.add('is-invalid');
            valid = false;
        } else if (panInput) {
            panInput.classList.remove('is-invalid');
        }
        if (!valid) e.preventDefault();
    });
});

