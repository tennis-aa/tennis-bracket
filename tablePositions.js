let draws;
let results;
let points_per_round;

promise1 = fetch("ao2021_draws.json").then((response)=>response.json()
).then(function (p){
  draws = p;
});
promise2 = fetch("ao2021_results.json").then((response)=>response.json()
).then(function(p){
  results=p; 
});
promise3 = fetch("config.json").then((response)=>response.json()
).then(function(p) {
  points_per_round = p["points_per_round"];
});

Promise.all([promise1,promise2,promise3]).then(function() {
  console.log(draws);
  console.log(results);
  console.log(points_per_round);
}).then(function() {
  let entries = [];
  for (let key in draws) {
    let points = computePoints(draws[key],results,points_per_round);
    entries.push({user: key, points: points,position: 1});
  }
  entries.sort(function(a,b) {
    return b.points - a.points;
  });
  nr_users = entries.length;
  for (let i=1;i<nr_users;i++) {
    if (entries[i].points == entries[i-1].points) {
      entries[i].position = entries[i-1].position
    } else {
      entries[i].position = i + 1;
    }
  }
  console.log(entries)


  for (let i=0; i<entries.length; i++) {
    table_row = document.createElement("tr");
    // Add position
    table_entry = document.createElement("td");
    table_entry.appendChild(document.createTextNode(entries[i].position))
    table_row.appendChild(table_entry)

    // Add user name
    table_entry = document.createElement("td");
    table_entry.appendChild(document.createTextNode(entries[i].user))
    table_row.appendChild(table_entry)

    // Add points
    table_entry = document.createElement("td");
    table_entry.appendChild(document.createTextNode(entries[i].points))
    table_row.appendChild(table_entry)

    // Add rank
    table_entry = document.createElement("td");
    let rank;
    if (entries[i].position <= nr_users/2) {
      rank = "top " + (entries[i].position/nr_users*100) + "%";
    } else {
      rank = "bot " + ((nr_users - entries[i].position + 1)/nr_users*100) + "%";
    }
    table_entry.appendChild(document.createTextNode(rank))
    table_row.appendChild(table_entry)

    // Add row to table
    table = document.getElementById("table-positions")
    table.appendChild(table_row)
  }
});

// .then(function(){
//   for (let i=0; i<draws.length;i++) {
//     points[user]
//   }
//   let tab = document.getElementById("table-positions");
// })

// Promise.all([
//   fetch("draws_examples/draws.json"),
//   fetch("results.json"),
//   fetch("config.json")
// ]).then(function(responses) {
//   return [
//     responses[0].json(),
//     responses[1].json(),
//     responses[2].json()
//   ]
// }).then(function(p) {
//   draws = p[0];
//   results = p[1];
//   points_per_round = p[2]["points_per_round"];
// }).then(function(){
//   console.log(draws);
//   console.log(results);
//   console.log(points_per_round);
// })