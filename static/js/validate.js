document.addEventListener('DOMContentLoaded', function () {
                    // First and Last Name validation
                    const nameInputs = [document.getElementById('inputFirstName'), document.getElementById('inputLastName')];
                    nameInputs.forEach(input => {
                        input.addEventListener('input', function () {
                            this.value = this.value.replace(/[^A-Za-z]/g, '');
                        });
                    }); // <-- Fixed: closed forEach

                    // Aadhaar validation
                    const adharInput = document.getElementById('adhar');
                    if (adharInput) {
                        adharInput.addEventListener('input', function () {
                            // Remove all non-digit characters
                            let digits = this.value.replace(/\D/g, '').slice(0, 12);
                            // Format as xxxx xxxx xxxx
                            let formatted = digits.replace(/(.{4})/g, '$1 ').trim();
                            this.value = formatted;
                            // Set validity: valid only if 12 digits
                            if (digits.length !== 12) {
                                this.setCustomValidity('Aadhaar number must be exactly 12 digits');
                            } else {
                                this.setCustomValidity('');
                            }
                        });

                        // Prevent non-numeric keypresses
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
                            this.value = this.value.replace(/[^A-Za-z0-9]/g, '').slice(0, 10);
                        });
                    }

                    // Password match validation


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
                            const select = document.getElementById(drop.selectId); // Fixed: use selectId
                            if (select && !select.value) {
                                select.classList.add('is-invalid');
                                valid = false;
                            } else if (select) {
                                select.classList.remove('is-invalid');
                            }
                        });
                        if (!valid) {
                            e.preventDefault();
                        }
                    });
                });