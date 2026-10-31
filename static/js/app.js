document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("assessment-form");
    const strategySelect = document.getElementById("strategy-select");
    const alertBox = document.getElementById("alert-box");

    // Load initial state on startup
    fetchReport();

    // Submit Assessment Form
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const data = {
            name: document.getElementById("name").value,
            score: document.getElementById("score").value,
            max_score: document.getElementById("max_score").value,
            weight: document.getElementById("weight").value
        };

        const res = await fetch("/api/add-assessment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        
        if (res.ok) {
            showAlert(result.message, "success");
            form.reset();
            document.getElementById("score").value = "85";
            document.getElementById("max_score").value = "100";
            document.getElementById("weight").value = "0.25";
            fetchReport();
        } else {
            showAlert(`❌ ${result.message}`, "error");
        }
    });

    // Strategy Switching
    strategySelect.addEventListener("change", async (e) => {
        const strategy = e.target.value;

        const res = await fetch("/api/set-strategy", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ strategy })
        });

        const result = await res.json();
        if (res.ok) {
            showAlert(result.message, "success");
            fetchReport();
        } else {
            showAlert(result.message, "error");
        }
    });

    // Fetch live standing from backend service
    async function fetchReport() {
        const res = await fetch("/api/report");
        const data = await res.json();

        const report = data.report;
        const assessments = data.assessments;

        // Update metrics
        document.getElementById("metric-percentage").textContent = `${report.final_percentage}%`;
        document.getElementById("metric-gpa").textContent = report.calculated_gpa.toFixed(2);
        
        const statusElem = document.getElementById("metric-status");
        statusElem.textContent = report.status;
        statusElem.style.color = report.status === "PASSED" ? "#4ade80" : "#f87171";

        document.getElementById("active-strategy").textContent = report.strategy_used;

        // Render Table
        const tbody = document.getElementById("assessment-table-body");
        tbody.innerHTML = "";

        if (assessments.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="empty-msg">No assessments recorded yet.</td></tr>`;
            return;
        }

        assessments.forEach(a => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${a.name}</td>
                <td>${a.score} / ${a.max_score}</td>
                <td>${a.percentage}%</td>
                <td>${a.weight}</td>
            `;
            tbody.appendChild(row);
        });
    }

    function showAlert(msg, type) {
        alertBox.textContent = msg;
        alertBox.className = `alert ${type}`;
        setTimeout(() => {
            alertBox.className = "alert hidden";
        }, 4000);
    }
    function switchView(viewName) {
  document.querySelectorAll('.view-panel').forEach(panel => {
    panel.classList.add('hidden');
    panel.classList.remove('active');
  });
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.classList.remove('active');
  });

  const activePanel = document.getElementById(`view-${viewName}`);
  if (activePanel) {
    activePanel.classList.remove('hidden');
    activePanel.classList.add('active');
  }
}
});
