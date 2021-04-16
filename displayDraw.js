let players;
// Put players in the draw
fetch("players.json").then((response)=>response.json()
).then(function (p){
  players = p;
  for (let i = 0; i < p.length; i++) {
    let id = "p" + i;
    document.getElementById(id).innerHTML = p[i];
  }
})

// Put picks in the draw
fetch("draws_examples/draws.json").then((response)=>response.json() 
).then(function (draws){
  let draw = draws[Object.keys(draws)[3]];
  let bracketSize = draw.length+1;
  for (let i = 0; i < draw.length; i++) {
    let id = "p" + (i+bracketSize)
    document.getElementById(id).innerHTML = draw[i]
  }
});
