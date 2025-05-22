// static/js/script.js

function validatePasswordMatch() {
    const pwd = document.querySelector('input[name="password"]');
    const cpwd = document.querySelector('input[name="confirm_password"]');
    if (pwd.value !== cpwd.value) {
        alert("Passwords do not match!");
        return false;
    }
    return true;
}
function validateForm() {
    const form = document.getElementById('user-form');
    const name = form.name.value;
    const email = form.email.value;
    const password = form.password.value;
    const confirmPassword = form.confirm_password.value;

    if (!name || !email || !password || !confirmPassword) {
        alert("All fields are required!");
        return false;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false;
    }

    return true;
}