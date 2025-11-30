let tasks = [];

function addTask() {
    const task = {
        id: "t" + (tasks.length + 1),
        title: document.getElementById("title").value,
        due_date: document.getElementById("due").value,
        estimated_hours: parseFloat(document.getElementById("hours").value),
        importance: parseInt(document.getElementById("importance").value),
        dependencies: document.getElementById("deps").value
            .split(",")
            .map(d => d.trim())
            .filter(d => d !== "")
    };

    tasks.push(task);
    alert("Task Added!");
}

function loadBulk() {
    try {
        const data = JSON.parse(document.getElementById("bulk").value);
        tasks = data;
        alert("Bulk tasks loaded!");
    } catch (e) {
        alert("Invalid JSON");
    }
}

function loadExample() {
    document.getElementById("bulk").value = `
[
  {
    "id": "t1",
    "title": "Fix login bug",
    "due_date": "2025-11-30",
    "estimated_hours": 2,
    "importance": 8,
    "dependencies": []
  },
  {
    "id": "t2",
    "title": "Prepare report",
    "due_date": "2025-11-25",
    "estimated_hours": 5,
    "importance": 7,
    "dependencies": ["t1"]
  }
]`;
}

async function analyze() {
    if (tasks.length === 0) {
        alert("No tasks to analyze!");
        return;
    }

    const strategy = document.getElementById("strategy").value;

    let response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tasks)
    });

    let result = await response.json();

    if (strategy === "fast") {
        result.sort((a, b) => a.estimated_hours - b.estimated_hours);
    }
    else if (strategy === "impact") {
        result.sort((a, b) => b.importance - a.importance);
    }
    else if (strategy === "deadline") {
        result.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    }
  
    showResults(result);
}

function showResults(result) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    result.forEach(task => {
        const div = document.createElement("div");
        div.classList.add("result");

        if (task.score >= 60) div.classList.add("high");
        else if (task.score >= 40) div.classList.add("medium");
        else div.classList.add("low");

        div.innerHTML = `
            <h3>${task.title}</h3>
            <p><strong>Score:</strong> ${task.score}</p>
            <p><strong>Due:</strong> ${task.due_date || "None"}</p>
            <p><strong>Hours:</strong> ${task.estimated_hours}</p>
            <p><strong>Importance:</strong> ${task.importance}</p>
            <p><strong>Dependencies:</strong> ${task.dependencies.join(", ")}</p>
        `;

        container.appendChild(div);
    });
}
