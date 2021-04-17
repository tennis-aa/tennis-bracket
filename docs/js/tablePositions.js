let brackets;
let results;
let table_results;

function loadTable() {
  promise3 = fetch("table_results.json").then((response)=>response.json()
  ).then(function(p) {
    table_results = p;
  }).then(function() {
    let nr_users = table_results.user.length;
    for (let i=0; i<nr_users; i++) {
      table_row = document.createElement("tr");
      // Add position
      table_entry = document.createElement("td");
      table_entry.appendChild(document.createTextNode(table_results.position[i]))
      table_row.appendChild(table_entry)

      // Add user name
      table_entry = document.createElement("td");
      table_entry.appendChild(document.createTextNode(table_results.user[i]))
      table_row.appendChild(table_entry)

      // Add points
      table_entry = document.createElement("td");
      table_entry.appendChild(document.createTextNode(table_results.points[i]))
      table_row.appendChild(table_entry)

      // Add rank
      table_entry = document.createElement("td");
      table_entry.appendChild(document.createTextNode(table_results.rank[i]))
      table_row.appendChild(table_entry)

      // Add row to table
      table = document.getElementById("table-positions")
      table.appendChild(table_row)
    }
  });
}
