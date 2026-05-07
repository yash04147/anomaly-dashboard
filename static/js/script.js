function getTeamClass(team) {
  if (!team) return "";

  team = team.toLowerCase();

  if (team.includes("dba")) return "team-dba";
  if (team.includes("oms")) return "team-oms";

  return "team-third";
}

function loadTab(system, element) {

  document
    .querySelectorAll(".tab")
    .forEach(tab => tab.classList.remove("active"));

  element.classList.add("active");

  fetch(`/api/anomalies/${system}`)
    .then(res => res.json())
    .then(data => {

      const table = document.querySelector("table");

      // No data
      if (data.length === 0) {
        table.innerHTML = "<tr><td>No Data</td></tr>";
        return;
      }

      // Dynamically create columns
      const columns = Object.keys(data[0]);

      let thead = "<thead><tr>";

      columns.forEach(col => {
        thead += `<th>${col}</th>`;
      });

      thead += "</tr></thead>";

      // Create rows
      let tbody = "<tbody>";

      data.forEach(row => {

        tbody += "<tr>";

        columns.forEach(col => {
          tbody += `<td>${row[col]}</td>`;
        });

        tbody += "</tr>";
      });

      tbody += "</tbody>";

      table.innerHTML = thead + tbody;
    });
}

// Load default tab
window.onload = function () {
  loadTab("Database", document.querySelector(".tab"));
};