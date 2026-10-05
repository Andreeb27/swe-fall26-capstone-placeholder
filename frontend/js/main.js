import { getHealth } from "./api.js";

const statusEl = document.getElementById("backend-status");

async function checkBackend() {
    statusEl.className = "status";
    try {
        const health = await getHealth();
        statusEl.textContent = `Backend: ${health.status} (scale: ${health.scale_driver})`;
        statusEl.classList.add("ok");
    } catch (err) {
        statusEl.textContent = "Backend: unreachable (is uvicorn running?)";
        statusEl.classList.add("error");
    }
}

document.getElementById("demo-btn").addEventListener("click", checkBackend);
checkBackend();
