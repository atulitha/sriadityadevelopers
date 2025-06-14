document.addEventListener('DOMContentLoaded', function () {
                    // First and Last Name validation
                    ['inputFirstName', 'inputLastName'].forEach(function(id) {
                        const input = document.getElementById(id);
                        if (input) {
                            input.addEventListener('input', function () {
                                this.value = this.value.replace(/[^A-Za-z]/g, '');
                            });
                        }
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
                        const input = toggle.previousElementSibling;
                        if (input) {
                            toggle.addEventListener('click', function() {
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
                        }
                    });

                    // Dropdowns: show selected value in field box
                    [
                        { selectId: 'gender', displayId: 'gender_display' },
                        { selectId: 'designation', displayId: 'designation_display' },
                        { selectId: 'Reference_agent', displayId: 'Reference_agent_display' },
                        { selectId: 'Agent_team', displayId: 'Agent_team_display' }
                    ].forEach(function(drop) {
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
                    const dateInput = document.getElementById("dateOfVisit");
                    const dateError = document.getElementById("dateError");

                    // Function to get today's date in YYYY-MM-DD format
                    function getTodayString() {
                        const today = new Date();
                        const yyyy = today.getFullYear();
                        const mm = String(today.getMonth() + 1).padStart(2, '0');
                        const dd = String(today.getDate()).padStart(2, '0');
                        return `${yyyy}-${mm}-${dd}`;
                    }

                    const todayStr = getTodayString();
                    dateInput.min = todayStr; // disable past dates in calendar picker

                    function isPast(selectedDate) {
                        return selectedDate < todayStr;
                    }

                    // Real-time input validation
                    dateInput.addEventListener("input", function () {
                        const selectedDate = dateInput.value;
                        if (isPast(selectedDate)) {
                            dateError.textContent = "Past dates are strictly not allowed.";
                            dateError.style.display = "block";
                            dateInput.value = "";
                        } else {
                            dateError.textContent = "";
                            dateError.style.display = "none";
                        }
                    });

                    // Validate on form submission too
                    const form = dateInput.closest("form");
                    if (form) {
                        form.addEventListener("submit", function (e) {
                            const selectedDate = dateInput.value;
                            if (isPast(selectedDate)) {
                                e.preventDefault();
                                dateError.textContent = "Please select today or a future date.";
                                dateError.style.display = "block";
                                dateInput.focus();
                            }
                        });
                    }

                    // Password validation with tick marks
                    const passwordInput = document.getElementById("inputPassword");
                    const confirmPasswordInput = document.getElementById("inputConfirmPassword");
                    const confirmPasswordError = document.getElementById("confirmPasswordError");

                    function createTick(input) {
                        let tick = document.createElement('span');
                        tick.textContent = '✔️';
                        tick.style.display = 'none';
                        input.parentNode.appendChild(tick);
                        return tick;
                    }

                    let passwordTick = passwordInput ? createTick(passwordInput) : null;
                    let confirmTick = confirmPasswordInput ? createTick(confirmPasswordInput) : null;

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
                            if (passwordInput) passwordInput.style.border = "2px solid red";
                            if (confirmPasswordInput) confirmPasswordInput.style.border = "2px solid red";
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
                            if (errorDiv) {
                                if (address.length > 128) {
                                    errorDiv.textContent = 'Address cannot exceed 128 characters.';
                                    errorDiv.style.display = 'block';
                                } else {
                                    errorDiv.textContent = '';
                                    errorDiv.style.display = 'none';
                                }
                            }
                        });
                    }

                    // Agent-sales page: dynamic dropdowns
                    const mainDropdown = document.getElementById('mainDropdown');
                    if (mainDropdown) {
                        mainDropdown.innerHTML = `
                            <option value="">Select Project</option>
                            <option value="nandagokulam">Nanda Gokulam</option>
                            <option value="panasapadu">Panasapadu</option>
                        `;
                    }

                    if (mainDropdown) {
                        Promise.all([
                            fetch('/test?key=sub1Options').then(res => res.json()),
                            fetch('/test?key=sub2Options').then(res => res.json())
                        ]).then(([sub1, sub2]) => {
                            window.sub1Options = sub1.sub1Options;
                            window.sub2Options = sub2.sub2Options;

                            const sub1Dropdown = document.getElementById('sub1Dropdown');
                            const sub2Dropdown = document.getElementById('sub2Dropdown');
                            const sub1Group = document.getElementById('sub1Group');
                            const sub2Group = document.getElementById('sub2Group');
                            const sub1Label = document.querySelector('label[for="sub1Dropdown"]');
                            const sub2Label = document.querySelector('label[for="sub2Dropdown"]');
                            const plotSizeInput = document.getElementById('plotSizeInput');
                            const plotSizeUnit = document.getElementById('plotSizeUnit');

                            if (plotSizeInput) plotSizeInput.readOnly = true;

                            if (mainDropdown && sub1Dropdown && sub2Dropdown && sub1Group && sub2Group && sub1Label && sub2Label && plotSizeInput) {
                                mainDropdown.addEventListener('change', function() {
                                    const val = this.value;
                                    sub1Dropdown.innerHTML = '<option value="">Select Sub Option 1</option>';
                                    sub2Dropdown.innerHTML = '<option value="">Select Sub Option 2</option>';
                                    sub1Group.style.display = 'none';
                                    sub2Group.style.display = 'none';
                                    plotSizeInput.value = '';
                                    if (plotSizeUnit) plotSizeUnit.textContent = '';
                                    sub1Label.textContent = val && mainDropdown.options[mainDropdown.selectedIndex]
                                        ? mainDropdown.options[mainDropdown.selectedIndex].text
                                        : '';
                                    if (sub2Label) sub2Label.textContent = '';
                                    if (window.sub1Options[val]) {
                                        window.sub1Options[val].forEach(opt => {
                                            sub1Dropdown.innerHTML += `<option value="${opt.value}">${opt.text}</option>`;
                                        });
                                        sub1Group.style.display = '';
                                    }
                                });

                                sub1Dropdown.addEventListener('change', function() {
                                    const val = this.value;
                                    sub2Dropdown.innerHTML = '<option value="">Select Sub Option 2</option>';
                                    sub2Group.style.display = 'none';
                                    plotSizeInput.value = '';
                                    if (plotSizeUnit) plotSizeUnit.textContent = '';
                                    sub2Label.textContent = val && this.options[this.selectedIndex]
                                        ? this.options[this.selectedIndex].text
                                        : '';
                                    if (window.sub2Options[val]) {
                                        window.sub2Options[val].forEach(opt => {
                                            sub2Dropdown.innerHTML += `<option value="${opt.value}">${opt.text}</option>`;
                                        });
                                        sub2Group.style.display = '';
                                    }
                                });

                                sub2Dropdown.addEventListener('change', function() {
                                    const sub1Val = sub1Dropdown.value;
                                    const val = this.value;
                                    plotSizeInput.value = '';
                                    if (plotSizeUnit) plotSizeUnit.textContent = '';
                                    const sub2Options = window.sub2Options[sub1Val] || [];
                                    const selected = sub2Options.find(opt => opt.value === val);
                                    if (selected && selected.size) {
                                        let unit = '';
                                        if (sub1Val === 'plots_pns') {
                                            unit = 'sq yards';
                                        } else if (sub1Val === 'villas_ng' || sub1Val === 'Flats_ng') {
                                            unit = 'sq feet';
                                        }
                                        plotSizeInput.value = selected.size + unit;
                                    }
                                    plotSizeInput.readOnly = true;
                                });
                            }
                        });
                    }

                    // Agent-sales page: set today's date for bookingDateInput
                    const bookingDateInput = document.getElementById('bookingDateInput');
                    if (bookingDateInput) {
                        const today = new Date().toISOString().split('T')[0];
                        bookingDateInput.value = today;
                    }

                    // Agent-sales page total plot value calculation
                    function updateTotalPlotValue() {
                        const sizeElem = document.getElementById('plotSizeInput');
                        const priceElem = document.getElementById('plotPriceInput');
                        const totalElem = document.getElementById('totalPlotValueInput');
                        if (sizeElem && priceElem && totalElem) {
                            const size = parseFloat(sizeElem.value) || 0;
                            const price = parseFloat(priceElem.value) || 0;
                            totalElem.value = size * price;
                        }
                    }
                    const plotSizeInputElem = document.getElementById('plotSizeInput');
                    const plotPriceInputElem = document.getElementById('plotPriceInput');
                    if (plotSizeInputElem) plotSizeInputElem.addEventListener('input', updateTotalPlotValue);
                    if (plotPriceInputElem) plotPriceInputElem.addEventListener('input', updateTotalPlotValue);

                    // Agent sales page final sale
                    function updateFinalSalePrice() {
                        const totalElem = document.getElementById('totalPlotValueInput');
                        const discountElem = document.getElementById('discountInput');
                        const finalElem = document.getElementById('finalSalePriceInput');
                        if (totalElem && discountElem && finalElem) {
                            const total = parseFloat(totalElem.value) || 0;
                            const discount = parseFloat(discountElem.value) || 0;
                            finalElem.value = total - discount;
                        }
                    }
                    const totalPlotValueInputElem = document.getElementById('totalPlotValueInput');
                    const discountInputElem = document.getElementById('discountInput');
                    if (totalPlotValueInputElem) totalPlotValueInputElem.addEventListener('input', updateFinalSalePrice);
                    if (discountInputElem) discountInputElem.addEventListener('input', updateFinalSalePrice);
                });