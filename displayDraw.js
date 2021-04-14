let players
// Put players in the draw
fetch("players.json").then((response)=>response.json()
).then(function (p){
  players = p;
  for (let i = 0; i < p.length; i++) {
    let id = "p" + i;
    document.getElementById(id).innerHTML = p[i];
  }
  return fetch("picks.json")
}).then((response)=>response.json() // Put picks in the draw
).then(function (p){
  let bracketSize = players.length;
  for (let i = 0; i < p.length; i++) {
    let id = "p" + (i+bracketSize)
    document.getElementById(id).innerHTML = p[i]
  }
  console.log(players)
});
console.log("hi")