let players;
let bracket;
let results;
let bracketSize
// Put players in the bracket
promise1 = fetch("players.json").then((response)=>response.json()
).then(function (p){
  players = p;
  for (let i = 0; i < p.length; i++) {
    let id = "p" + i;
    document.getElementById(id).innerHTML = p[i];
  }
})

// Put picks in the bracket
promise2 = fetch("brackets_examples/brackets.json").then((response)=>response.json() 
).then(function (brackets){
  bracket = brackets[Object.keys(brackets)[1]];
  bracketSize = bracket.length+1;
  for (let i = 0; i < bracket.length; i++) {
    let id = "p" + (i+bracketSize)
    document.getElementById(id).innerHTML = bracket[i]
  }
});

promise3 = fetch("results.json").then((response)=>response.json()
).then(function(p){
  results = p;
});


Promise.all([promise2,promise3]).then(function(){
  for (let i = 0; i < bracket.length; i++) {
    let id = "p" + (i+bracketSize)
    if (results[i]!="" && bracket[i]==results[i]) {
      document.getElementById(id).style.color = "green"
    } else if (results[i]!="" && bracket[i]!=results[i]){
      document.getElementById(id).style.color = "red"
    }
  }
})