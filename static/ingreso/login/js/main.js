
document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const togglePasswordButton = document.getElementById('togglePassword');

    togglePasswordButton.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);

        // Cambiar el ícono del ojo entre abierto y cerrado
        const eyeIconClass = type === 'password' ? 'fa-eye' : 'fa-eye-slash';
        togglePasswordButton.classList.remove('fa-eye', 'fa-eye-slash');
        togglePasswordButton.classList.add(eyeIconClass);
    });
});
