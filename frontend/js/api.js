// The only place that knows backend URLs. Same origin in dev: FastAPI serves this frontend.
export async function getHealth() {
    const response = await fetch("/api/health");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
}
