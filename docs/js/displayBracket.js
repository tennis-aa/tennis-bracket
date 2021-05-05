let players;
let brackets;
let results;
let scores;
let losers;
let table_results
let bracketSize;
// Put players in the bracket
function loadDisplay() {
  bracketSize = Number(document.getElementById("bracket-size").innerHTML);
  promise1 = fetch("./players.json").then((response)=>response.json()
  ).then(function (p){
    players = p["players"];
    for (let i = 0; i < players.length; i++) {
      let id = "p" + i;
      document.getElementById(id).innerHTML = players[i];
    }
  });

  promise2 = fetch("./brackets.json").then((response)=>response.json() 
  ).then(function (response){
    brackets = response;
    let sel = document.getElementById("user");
    let users = Object.keys(brackets);
    users.sort();
    for (let i=0; i<users.length; i++) {
      let opt = document.createElement("option");
      opt.innerHTML = users[i];
      sel.appendChild(opt)
    }
  });

  promise3 = fetch("./results.json").then((response)=>response.json()
  ).then(function(p){
    results = p["results"];
    scores = p["scores"];
    losers = p["losers"];
    table_results = p["table_results"];
    for (let i = 0; i < results.length; i++) {
      let id = "p" + (i+bracketSize);
      document.getElementById(id).innerHTML = results[i];
  }
  });

  // promise4 = fetch("./table_results.json").then((response)=> response.json()
  // ).then(function(response) {
  //   table_results = response;
  // });

  Promise.all([promise2,promise3]).then(function() {
    let params = new URLSearchParams(location.search);
    let sel = document.getElementById("user");
    sel.value = params.get("user");
    sel.onchange();
  })
}

function display_bracket() {
  let user = document.getElementById("user").value;
  let user_info = document.getElementById("user-info");
  if (user==""){
    user_info.innerHTML = "";
    for (let i = 0; i < results.length; i++) {
      let player = document.getElementById("p" + (i+bracketSize));
      player.innerHTML = results[i];
      player.style.color = "black";
    }
  } else {
    let bracket = brackets[user];
    let user_loc = table_results.user.findIndex(element=> element==user);
    let nr_users = table_results.user.length;
    user_info.innerHTML =  table_results.points[user_loc] + " puntos" + "<br>" + "Posicion " + table_results.position[user_loc] + "/" + nr_users + " (" + table_results.rank[user_loc] + ")";
    for (let i = 0; i < bracket.length; i++) {
      let player = document.getElementById("p" + (i+bracketSize));
      player.innerHTML = bracket[i];
      if (i<bracketSize/2 && (players[2*i]=="Bye" || players[2*i+1]=="Bye")) {
        console.log(i)
        player.style.color = "black";
      } else if (results[i]!="" && bracket[i]==results[i]) {
        player.style.color = "green";
      } else if (losers.includes(bracket[i])){
        player.style.color = "red";
      } else {
        player.style.color = "black";
      }
    }
  }
}
