document.getElementById("form").addEventListener("submit", async function(e){
    e.preventDefault();

    const data = {
        skill: document.getElementById("skill").value,
        level: document.getElementById("level").value,
        semesters: document.getElementById("semesters").value,
        hours: document.getElementById("hours").value,
        focus: document.getElementById("focus").value
    };

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("API Response:", result);

        const output = document.getElementById("output");
        output.innerHTML = "";

        if (result.error) {
            output.innerHTML = "<p>Generation failed. Try again.</p>";
            return;
        }

        // Handle both possible structures safely
        const curriculum = result.curriculum ? result.curriculum : result;

        if (!curriculum.courses || !Array.isArray(curriculum.courses)) {
            output.innerHTML = "<p>No courses found in response.</p>";
            console.error("Invalid structure:", curriculum);
            return;
        }

        // Title Section
        output.innerHTML += `<h2>${(curriculum.domain || "Curriculum").toUpperCase()}</h2>`;
        output.innerHTML += `<p><strong>Level:</strong> ${curriculum.level || "N/A"}</p>`;
        output.innerHTML += `<p><strong>Industry Focus:</strong> ${curriculum.industryOrientation || "N/A"}</p>`;
        output.innerHTML += `<p><strong>Total Semesters:</strong> ${curriculum.semesters || curriculum.courses.length}</p>`;
        output.innerHTML += `<p><strong>Weekly Hours:</strong> ${curriculum.weeklyHours || "N/A"}</p>`;

        // Loop through semesters
        curriculum.courses.forEach(sem => {
            output.innerHTML += `<hr>`;
            output.innerHTML += `<div class="semester"><h3>Semester ${sem.semester}</h3>`;
        
            if (!sem.courses || !Array.isArray(sem.courses)) return;
        
            sem.courses.forEach(course => {
                output.innerHTML += `
                    <div class="course">
                        <strong>${course.name}</strong>
                        <p>Type: ${course.type || "N/A"}</p>
                        <p>Description: ${course.description || "N/A"}</p>
                        <p>Hours/Week: ${course.hoursPerWeek || "N/A"}</p>
                    </div>
                `;
            });
        
            output.innerHTML += `</div>`;
        });

    } catch (error) {
        console.error("Error:", error);
        document.getElementById("output").innerHTML =
            "<p>Something went wrong. Check console.</p>";
    }
});