document.addEventListener('DOMContentLoaded', function () {
    // First and Last Name validation
    const nameInputs = [document.getElementById('inputFirstName'), document.getElementById('inputLastName')];
    nameInputs.forEach(input => {
        if (input) {
            input.addEventListener('input', function () {
                this.value = this.value.replace(/[^A-Za-z]/g, '');
            });
        }
    });
    //Id validation
const combinedInput = document.getElementById('inputCombined');
const combinedError = document.getElementById('combinedError');

if (combinedInput) {
    combinedInput.addEventListener('input', function () {
        const prefixPatterns = {
            'CS': 13, // CS requires 12 characters
            'AG': 9,  // AG requires 8 characters
            'MG': 9,  // MG requires 8 characters
            'TL': 9,  // TL requires 8 characters
            'DR': 9,  // DR requires 8 characters
            'MD': 9,   // MD requires 8 characters
        };

        // Convert input to uppercase
        this.value = this.value.toUpperCase();
        const inputValue = this.value.trim();
        const regex = /^([A-Z]{2})-(\d+)$/; // Format: Prefix-Number
        const match = inputValue.match(regex);

        if (match) {
            const prefix = match[1];
            const number = match[2];

            if (prefixPatterns[prefix] && inputValue.length === prefixPatterns[prefix]) {
                combinedError.style.display = 'none';
                this.setCustomValidity('');
            } else {
                combinedError.textContent = `Invalid format. Prefix "${prefix}" requires ${prefixPatterns[prefix]} characters.`;
                combinedError.style.display = 'block';
                this.setCustomValidity('Invalid format.');
            }
        } else {
            combinedError.textContent = 'Invalid format. Use the format: Prefix-Number (e.g., CS-123456789012).';
            combinedError.style.display = 'block';
            this.setCustomValidity('Invalid format.');
        }
    });
}



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
            let raw = this.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
            let formatted = '';
            for (let i = 0; i < raw.length && i < 5; i++) {
                if (/[A-Z]/.test(raw[i])) formatted += raw[i];
            }
            for (let i = 5; i < raw.length && formatted.length < 9; i++) {
                if (/[0-9]/.test(raw[i])) formatted += raw[i];
            }
            for (let i = 9; i < raw.length && formatted.length < 10; i++) {
                if (/[A-Z]/.test(raw[i])) formatted += raw[i];
            }
            this.value = formatted;
            const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]$/;
            if (formatted.length === 10 && !panPattern.test(formatted)) {
                this.setCustomValidity('PAN must be 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)');
            } else {
                this.setCustomValidity('');
            }
        });
        panInput.addEventListener('keypress', function (e) {
            const char = e.key.toUpperCase();
            const value = panInput.value.toUpperCase();
            if (value.length >= 10) {
                e.preventDefault();
            } else if (value.length < 5 && !/[A-Z]/.test(char)) {
                e.preventDefault();
            } else if (value.length >= 5 && value.length < 9 && !/[0-9]/.test(char)) {
                e.preventDefault();
            } else if (value.length === 9 && !/[A-Z]/.test(char)) {
                e.preventDefault();
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

    // Date of visit validation: only allow booking from tomorrow onwards
    const dateInput = document.getElementById('dateOfVisit');
    if (dateInput) {
        function setMinDateToTomorrow() {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            const yyyy = tomorrow.getFullYear();
            const mm = String(tomorrow.getMonth() + 1).padStart(2, '0');
            const dd = String(tomorrow.getDate()).padStart(2, '0');
            const minDate = `${yyyy}-${mm}-${dd}`;
            dateInput.setAttribute('min', minDate);
            if (dateInput.value && dateInput.value < minDate) {
                dateInput.value = '';
            }
        }
        setMinDateToTomorrow();
        dateInput.addEventListener('input', function () {
            const selectedDate = new Date(this.value);
            const minAllowed = new Date(this.min);
            if (selectedDate < minAllowed) {
                alert('Invalid date. Please select a future date (from tomorrow onwards).');
                this.value = '';
            }
        });
    }

    // Password validation with tick marks
    const passwordInput = document.getElementById("inputPassword");
    const confirmPasswordInput = document.getElementById("inputConfirmPassword");
    const confirmPasswordError = document.getElementById("confirmPasswordError");
    let passwordTick, confirmTick;
    // Add fallback for missing createTick
    function dummyTick() { return { style: { display: "none" } }; }
    if (typeof createTick === 'function') {
        if (passwordInput) passwordTick = createTick(passwordInput);
        if (confirmPasswordInput) confirmTick = createTick(confirmPasswordInput);
    } else {
        passwordTick = dummyTick();
        confirmTick = dummyTick();
    }
    function validatePasswords() {
        if (!passwordInput || !confirmPasswordInput) return false;
        const pwd = passwordInput.value;
        const cpwd = confirmPasswordInput.value;
        if (pwd === cpwd && pwd.length > 0) {
            if (confirmPasswordError) confirmPasswordError.style.display = "none";
            passwordInput.style.border = "2px solid green";
            confirmPasswordInput.style.border = "2px solid green";
            if (passwordTick) passwordTick.style.display = "inline";
            if (confirmTick) confirmTick.style.display = "inline";
            return true;
        } else {
            if (confirmPasswordError) {
                confirmPasswordError.style.display = "block";
                confirmPasswordError.textContent = " Passwords do not match!";
            }
            passwordInput && (passwordInput.style.border = "2px solid red");
            confirmPasswordInput && (confirmPasswordInput.style.border = "2px solid red");
            if (passwordTick) passwordTick.style.display = "none";
            if (confirmTick) confirmTick.style.display = "none";
            return false;
        }
    }
    if (passwordInput) passwordInput.addEventListener("input", validatePasswords);
    if (confirmPasswordInput) confirmPasswordInput.addEventListener("input", validatePasswords);

    // Address validation
    const addressInput = document.getElementById('address');
    if (addressInput) {
        addressInput.addEventListener('input', function () {
            const address = this.value;
            const errorDiv = document.getElementById('addressError');
            if (!errorDiv) return;
            if (address.length > 128) {
                errorDiv.textContent = 'Address cannot exceed 128 characters.';
                errorDiv.style.display = 'block';
            } else {
                errorDiv.textContent = '';
                errorDiv.style.display = 'none';
            }
        });
    }

    // Agent-sales page: dynamic dropdowns (no nested DOMContentLoaded)
    function updatePlotSize(size, label) {
        const sizeInput = document.getElementById('plotSizeInput');
        const unitSpan = document.getElementById('plotSizeUnit');
        let unit = '';
        if (/plot/i.test(label)) {
            unit = 'sqyards';
        } else if (/flat|villa/i.test(label)) {
            unit = 'sqft';
        }
        if (sizeInput) sizeInput.value = size ? (size + unit) : '';
        if (unitSpan) unitSpan.textContent = '';
    }

    const mainDropdown = document.getElementById('mainDropdown');
    if (mainDropdown) {
        Promise.all([
            fetch('/test?key=sub1Options', { credentials: 'include' }),
            fetch('/test?key=sub2Options', { credentials: 'include' })
        ]).then(async ([res1, res2]) => {
            if (res1.status === 401 || res2.status === 401) {
                alert('Session expired or unauthorized. Please log in again.');
                window.location.href = '/login';
                return;
            }
            const sub1 = await res1.json();
            const sub2 = await res2.json();
            window.sub1Options = sub1.sub1Options || {};
            window.sub2Options = sub2.sub2Options || {};

            const sub1Dropdown = document.getElementById('sub1Dropdown');
            const sub2Dropdown = document.getElementById('sub2Dropdown');
            const sub1Group = document.getElementById('sub1Group');
            const sub2Group = document.getElementById('sub2Group');
            const sub1Label = sub1Group ? sub1Group.querySelector('label') : null;
            const sub2Label = sub2Group ? sub2Group.querySelector('label') : null;

            mainDropdown.addEventListener('change', function() {
                const val = this.value;
                const projectText = this.options[this.selectedIndex].text;
                if (sub1Dropdown && sub2Dropdown && sub1Group && sub2Group) {
                    sub1Dropdown.innerHTML = '<option value="">Select options</option>';
                    sub2Dropdown.innerHTML = '<option value="">Select options</option>';
                    sub1Group.style.display = 'none';
                    sub2Group.style.display = 'none';
                    if (sub1Label) sub1Label.textContent = '';
                    if (sub2Label) sub2Label.textContent = 'Options';
                    if (window.sub1Options[val]) {
                        window.sub1Options[val].forEach(opt => {
                            sub1Dropdown.innerHTML += `<option value="${opt.value}" data-size="${opt.size || ''}">${opt.text}</option>`;
                        });
                        sub1Group.style.display = '';
                        if (sub1Label) sub1Label.textContent = projectText;
                    }
                    updatePlotSize('', '');
                }
            });

            if (sub1Dropdown) {
                sub1Dropdown.addEventListener('change', function() {
                    const val = this.value;
                    const sub1Text = this.options[this.selectedIndex].text;
                    if (sub2Dropdown && sub2Group) {
                        sub2Dropdown.innerHTML = '<option value="">Select options</option>';
                        sub2Group.style.display = 'none';
                        if (sub2Label) sub2Label.textContent = 'Options';
                        if (window.sub2Options[val]) {
                            window.sub2Options[val].forEach(opt => {
                                sub2Dropdown.innerHTML += `<option value="${opt.value}" data-size="${opt.size || ''}">${opt.text}</option>`;
                            });
                            sub2Group.style.display = '';
                            if (sub2Label) sub2Label.textContent = sub1Text;
                        }
                    }
                    const selected = this.options[this.selectedIndex];
                    updatePlotSize(selected.getAttribute('data-size'), selected.text);
                });
            }

            if (sub2Dropdown) {
                sub2Dropdown.addEventListener('change', function() {
                    const selected = this.options[this.selectedIndex];
                    updatePlotSize(selected.getAttribute('data-size'), selected.text);
                });
            }
        }).catch(err => {
            console.error('Dropdown fetch error:', err);
        });
    }
    // Set booking date to today
    const bookingDateInput = document.getElementById('bookingDateInput');
    if (bookingDateInput) {
        const today = new Date().toISOString().split('T')[0];
        bookingDateInput.value = today;
    }

    // Agent-sales page total plot value calculation
    function updateTotalPlotValue() {
        const sizeInput = document.getElementById('plotSizeInput');
        const priceInput = document.getElementById('plotPriceInput');
        const totalInput = document.getElementById('totalPlotValueInput');
        if (sizeInput && priceInput && totalInput) {
            // Strip units explicitly
            const size = parseFloat((sizeInput.value || '').replace(/[^\d.]/g, '')) || 0;
            const price = parseFloat(priceInput.value) || 0;
            totalInput.value = size * price;
        }
    }
    const plotSizeInput = document.getElementById('plotSizeInput');
    const plotPriceInput = document.getElementById('plotPriceInput');
    if (plotSizeInput) plotSizeInput.addEventListener('input', updateTotalPlotValue);
    if (plotPriceInput) plotPriceInput.addEventListener('input', updateTotalPlotValue);

    // Agent-sales page final sale
    function updateFinalSalePrice() {
        const totalInput = document.getElementById('totalPlotValueInput');
        const discountInput = document.getElementById('discountInput');
        const finalInput = document.getElementById('finalSalePriceInput');
        if (totalInput && discountInput && finalInput) {
            const total = parseFloat(totalInput.value) || 0;
            const discount = parseFloat(discountInput.value) || 0;
            finalInput.value = total - discount;
        }
    }
    const totalPlotValueInput = document.getElementById('totalPlotValueInput');
    const discountInput = document.getElementById('discountInput');
    if (totalPlotValueInput) totalPlotValueInput.addEventListener('input', updateFinalSalePrice);
    if (discountInput) discountInput.addEventListener('input', updateFinalSalePrice);

    // Photo upload preview (safe for multi-page use)
    const photoInput = document.getElementById('photo_file');
    const photoPreview = document.getElementById('photo_preview');
    const removeBtn = document.getElementById('remove_photo');
    const placeholder = 'assets/img/profile_photo.png';

    if (photoInput && photoPreview && removeBtn) {
        photoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                if (!['image/jpeg', 'image/png'].includes(file.type)) {
                    alert('Only JPG and PNG files are allowed.');
                    photoInput.value = '';
                    photoPreview.src = placeholder;
                    removeBtn.style.display = 'none';
                    return;
                }
                if (file.size > 2 * 1024 * 1024) {
                    alert('File size must be less than 2MB.');
                    photoInput.value = '';
                    photoPreview.src = placeholder;
                    removeBtn.style.display = 'none';
                    return;
                }
                const reader = new FileReader();
                reader.onload = function(e) {
                    photoPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
                removeBtn.style.display = 'block';
            } else {
                photoPreview.src = placeholder;
                removeBtn.style.display = 'none';
            }
        });

        removeBtn.addEventListener('click', function() {
            photoInput.value = '';
            photoPreview.src = placeholder;
            removeBtn.style.display = 'none';
        });
    }

    // Phone validation
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.setAttribute('maxlength', '10');
        let errorDiv = document.getElementById('phoneError');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'phoneError';
            errorDiv.style.color = 'red';
            errorDiv.style.fontSize = '0.9em';
            phoneInput.parentNode.appendChild(errorDiv);
        }
        phoneInput.addEventListener('input', function () {
            this.value = this.value.replace(/\D/g, '').slice(0, 10);
            if (this.value.length !== 10 && this.value.length > 0) {
                errorDiv.textContent = "Phone number must be exactly 10 digits.";
                errorDiv.style.display = "block";
                this.setCustomValidity("Phone number must be exactly 10 digits.");
            } else {
                errorDiv.style.display = "none";
                this.setCustomValidity("");
            }
        });
        phoneInput.addEventListener('keypress', function (e) {
            if (!/\d/.test(e.key) || this.value.length >= 10) {
                e.preventDefault();
            }
        });
    }

    // Date of birth validation
    const dobInput = document.getElementById('dob');
    if (dobInput) {
        let errorDiv = document.getElementById('dobError');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'dobError';
            errorDiv.style.color = 'red';
            errorDiv.style.display = 'none';
            dobInput.parentNode.appendChild(errorDiv);
        }

        function updateDOBMax() {
            const now = new Date();
            const maxDate = new Date(now.getFullYear() - 18, now.getMonth(), now.getDate());
            dobInput.max = maxDate.toISOString().split('T')[0];
        }
        // Only set once, not every second
        updateDOBMax();

        dobInput.addEventListener('change', function () {
            const dob = new Date(this.value);
            const now = new Date();
            const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            const minAgeDate = new Date(now.getFullYear() - 18, now.getMonth(), now.getDate());
            errorDiv.style.display = 'none';

            // Prevent selecting today or any future date
            if (this.value === '' || dob.getTime() === today.getTime() || dob > today) {
                errorDiv.textContent = 'Please select a valid date of birth (not today or future).';
                errorDiv.style.display = 'block';
                this.value = '';
                this.classList.add('is-invalid');
                return;
            }
            if (dob > minAgeDate) {
                errorDiv.textContent = 'You must be at least 18 years old.';
                errorDiv.style.display = 'block';
                this.value = '';
                this.classList.add('is-invalid');
                return;
            }
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        });
    }
    // agentid validation
    const agentIdInput = document.getElementById('agentid');
    const AGENT_ID_PREFIX = 'AG-';
    const agentIdPattern = /^AG-\d{10}$/;

    if (agentIdInput) {
        // Set maxlength to 10 for digits only
        agentIdInput.setAttribute('maxlength', '10');

        // Insert fixed prefix as a visually left-aligned label if not already present
        let agPrefixSpan = document.getElementById('agent-id-prefix');
        if (!agPrefixSpan) {
            agPrefixSpan = document.createElement('span');
            agPrefixSpan.id = 'agent-id-prefix';
            agPrefixSpan.textContent = AGENT_ID_PREFIX;
            agPrefixSpan.style.marginRight = '4px';
            agPrefixSpan.style.fontWeight = 'bold';
            agPrefixSpan.style.display = 'inline-block';
            agPrefixSpan.style.verticalAlign = 'middle';

            // Wrap input and prefix in a container for better alignment
            const agWrapper = document.createElement('div');
            agWrapper.style.display = 'flex';
            agWrapper.style.alignItems = 'center';
            agWrapper.style.gap = '4px';

            agentIdInput.parentNode.insertBefore(agWrapper, agentIdInput);
            agWrapper.appendChild(agPrefixSpan);
            agWrapper.appendChild(agentIdInput);
        }

        // Style input to align with prefix
        agentIdInput.style.flex = '1 1 auto';
        agentIdInput.style.display = 'inline-block';

        agentIdInput.addEventListener('input', function () {
            // Only allow digits, max 10
            this.value = this.value.replace(/\D/g, '').slice(0, 10);
        });

        agentIdInput.addEventListener('blur', function () {
            const digits = this.value.trim();
            const agentId = AGENT_ID_PREFIX + digits;
            if (!agentIdPattern.test(agentId)) {
                agentIdInput.setCustomValidity('Agent ID must be AG- followed by exactly 10 digits.');
            } else {
                agentIdInput.setCustomValidity('');
            }
        });
    }

    // Customer ID validation (fixed prefix 'CS-')
    const customerIdInput = document.getElementById('customer-id');
    const customerDetailsDiv = document.getElementById('customer-id-details');
    const firstNameInput = document.getElementById('first-name');
    const lastNameInput = document.getElementById('last-name');
    const CUSTOMER_ID_PREFIX = 'CS-';
    const customerIdPattern = /^CS-\d{10}$/;

    if (customerIdInput) {
        // Set maxlength to 10 for digits only
        customerIdInput.setAttribute('maxlength', '10');

        // Insert fixed prefix as a visually left-aligned label if not already present
        let prefixSpan = document.getElementById('customer-id-prefix');
        if (!prefixSpan) {
            prefixSpan = document.createElement('span');
            prefixSpan.id = 'customer-id-prefix';
            prefixSpan.textContent = CUSTOMER_ID_PREFIX;
            prefixSpan.style.marginRight = '4px';
            prefixSpan.style.fontWeight = 'bold';
            prefixSpan.style.display = 'inline-block';
            prefixSpan.style.verticalAlign = 'middle';

            // Wrap input and prefix in a container for better alignment
            const wrapper = document.createElement('div');
            wrapper.style.display = 'flex';
            wrapper.style.alignItems = 'center';
            wrapper.style.gap = '4px';

            customerIdInput.parentNode.insertBefore(wrapper, customerIdInput);
            wrapper.appendChild(prefixSpan);
            wrapper.appendChild(customerIdInput);
        }

        // Style input to align with prefix
        customerIdInput.style.flex = '1 1 auto';
        customerIdInput.style.display = 'inline-block';

        customerIdInput.addEventListener('input', function () {
            // Only allow digits, max 10
            this.value = this.value.replace(/\D/g, '').slice(0, 10);
        });

        customerIdInput.addEventListener('blur', function () {
            const digits = this.value.trim();
            const customerId = CUSTOMER_ID_PREFIX + digits;
            if (customerIdPattern.test(customerId)) {
                fetch(`/get-customer-details?id=${customerId}`)
                    .then(response => {
                        if (!response.ok) throw new Error('Network response was not ok');
                        return response.json();
                    })
                    .then(data => {
                        if (data.status === 'success' && data.customer) {
                            if (customerDetailsDiv) customerDetailsDiv.style.display = 'block';
                            if (firstNameInput) firstNameInput.value = data.customer.firstName;
                            if (lastNameInput) lastNameInput.value = data.customer.lastName;
                        } else {
                            if (customerDetailsDiv) customerDetailsDiv.style.display = 'none';
                            alert('Customer not found');
                        }
                    })
                    .catch(error => {
                        console.error('Fetch error:', error);
                        if (customerDetailsDiv) customerDetailsDiv.style.display = 'none';
                        alert('An error occurred while fetching customer details');
                    });
            } else {
                if (customerDetailsDiv) customerDetailsDiv.style.display = 'none';
                alert('Invalid Customer ID format. Enter exactly 10 digits after CS-.');
            }
        });
    }

});