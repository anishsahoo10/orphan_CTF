/**
 * ORPHAN // AXIOM SYSTEMS ARCHIVAL PORTAL
 * Live clock and CCTV timestamp updates.
 */

(function () {
  "use strict";

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function updateTimers() {
    var now = new Date();
    var yyyy = now.getUTCFullYear();
    var mm = pad(now.getUTCMonth() + 1);
    var dd = pad(now.getUTCDate());
    var hh = pad(now.getUTCHours());
    var min = pad(now.getUTCMinutes());
    var ss = pad(now.getUTCSeconds());

    var timeStr = yyyy + "-" + mm + "-" + dd + " " + hh + ":" + min + ":" + ss + " UTC";

    var topClock = document.getElementById("sys-clock");
    if (topClock) topClock.textContent = timeStr;

    var cctvClock = document.getElementById("cctv-time");
    if (cctvClock) cctvClock.textContent = timeStr;
  }

  document.addEventListener("DOMContentLoaded", function () {
    updateTimers();
    setInterval(updateTimers, 1000);
  });
})();
