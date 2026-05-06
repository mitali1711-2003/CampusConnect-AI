/**
 * Session Timeout Warning — shows a modal after 30 min of inactivity.
 * Counts down 60 seconds, then redirects to /logout.
 * Any user interaction resets the timer.
 */
(function () {
    const IDLE_MS = 30 * 60 * 1000;   // 30 minutes
    const WARN_MS = 60 * 1000;         // 60-second countdown
    const LOGOUT_URL = '/logout';

    let idleTimer = null;
    let countdownTimer = null;
    let secondsLeft = 60;
    let modalVisible = false;

    // ── Build modal DOM once ───────────────────────────────────
    const overlay = document.createElement('div');
    overlay.id = 'sessionTimeoutOverlay';
    overlay.style.cssText = `
        display:none; position:fixed; inset:0;
        background:rgba(0,0,0,0.55); z-index:99999;
        align-items:center; justify-content:center;
    `;
    overlay.innerHTML = `
        <div style="
            background:#fff; border-radius:20px; padding:36px 32px;
            width:400px; max-width:92vw; text-align:center;
            box-shadow:0 20px 60px rgba(0,0,0,0.25);
            animation: slideUp 0.3s ease;
        ">
            <div style="font-size:48px; margin-bottom:12px;">⏱️</div>
            <h3 style="font-size:20px; font-weight:700; margin-bottom:8px; color:#2D3748;">
                Still there?
            </h3>
            <p style="color:#718096; font-size:15px; margin-bottom:6px;">
                You'll be logged out due to inactivity in
            </p>
            <p id="timeoutCountdown" style="
                font-size:42px; font-weight:800; color:#E27070;
                margin: 12px 0;
            ">60</p>
            <p style="color:#718096; font-size:13px; margin-bottom:24px;">seconds</p>
            <button id="stayLoggedInBtn" style="
                padding:12px 36px; border:none; border-radius:12px;
                background:linear-gradient(135deg,#5B7FD6,#4A6BBF);
                color:white; font-weight:700; font-size:15px; cursor:pointer;
                transition:all 0.2s;
            ">Stay Logged In</button>
            <div style="margin-top:12px;">
                <a href="${LOGOUT_URL}" style="color:#A0AEC0; font-size:13px;">
                    Log out now
                </a>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);

    document.getElementById('stayLoggedInBtn').addEventListener('click', resetTimer);

    // ── Show / hide modal ──────────────────────────────────────
    function showModal() {
        if (modalVisible) return;
        modalVisible = true;
        secondsLeft = 60;
        overlay.style.display = 'flex';
        document.getElementById('timeoutCountdown').textContent = secondsLeft;

        countdownTimer = setInterval(function () {
            secondsLeft--;
            const el = document.getElementById('timeoutCountdown');
            if (el) el.textContent = secondsLeft;
            if (secondsLeft <= 0) {
                clearInterval(countdownTimer);
                window.location.href = LOGOUT_URL;
            }
        }, 1000);
    }

    function hideModal() {
        modalVisible = false;
        overlay.style.display = 'none';
        clearInterval(countdownTimer);
    }

    // ── Reset idle timer on any user activity ──────────────────
    function resetTimer() {
        hideModal();
        clearTimeout(idleTimer);
        idleTimer = setTimeout(showModal, IDLE_MS);
    }

    // Listen to any meaningful user interaction
    ['mousemove', 'mousedown', 'keydown', 'touchstart', 'scroll', 'click'].forEach(function (evt) {
        document.addEventListener(evt, resetTimer, { passive: true });
    });

    // Kick off the idle timer on page load
    resetTimer();
})();
