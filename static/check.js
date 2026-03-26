        function togglePassword(inputId) {
            const input = document.getElementById(inputId);
            const icon = document.getElementById(`toggle${inputId.charAt(0).toUpperCase() + inputId.slice(1)}-icon`);
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        }
        
        const password = document.getElementById('password');
        const passwordConfirm = document.getElementById('password_confirm');
        const matchMsg = document.getElementById('passwordMatch');
        const noMatchMsg = document.getElementById('passwordNoMatch');
        const submitBtn = document.getElementById('submitBtn');
        
        function checkPasswordMatch() {
            if (passwordConfirm.value === '') {
                matchMsg.classList.add('hidden');
                noMatchMsg.classList.add('hidden');
                return;
            }
            
            if (password.value === passwordConfirm.value) {
                matchMsg.classList.remove('hidden');
                noMatchMsg.classList.add('hidden');
                passwordConfirm.classList.add('input-valid');
                passwordConfirm.classList.remove('input-invalid');
                submitBtn.disabled = false;
            } else {
                matchMsg.classList.add('hidden');
                noMatchMsg.classList.remove('hidden');
                passwordConfirm.classList.add('input-invalid');
                passwordConfirm.classList.remove('input-valid');
                submitBtn.disabled = true;
            }
        }
        
        password.addEventListener('input', checkPasswordMatch);
        passwordConfirm.addEventListener('input', checkPasswordMatch);
        
        const username = document.getElementById('username');
        username.addEventListener('input', function() {
            if (this.validity.patternMismatch) {
                this.classList.add('input-invalid');
                this.classList.remove('input-valid');
            } else if (this.value.length >= 3) {
                this.classList.add('input-valid');
                this.classList.remove('input-invalid');
            } else {
                this.classList.remove('input-valid', 'input-invalid');
            }
        });

        const email = document.getElementById('email');
        email.addEventListener('input', function() {
            if (this.validity.typeMismatch || this.validity.valueMissing) {
                this.classList.add('input-invalid');
                this.classList.remove('input-valid');
            } else if (this.value.length > 0) {
                this.classList.add('input-valid');
                this.classList.remove('input-invalid');
            }
        });