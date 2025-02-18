// Auto Logout Timer
let logoutTimer;

function resetLogoutTimer() {
    clearTimeout(logoutTimer);
    logoutTimer = setTimeout(function() {
        window.location.href = "/accounts/logout/";
    }, 900000);
}

// Reset timer on user input
window.onload = resetLogoutTimer;
document.onmousemove = resetLogoutTimer;
document.onkeydown = resetLogoutTimer;
document.oninput = resetLogoutTimer;
