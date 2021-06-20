let bracketSize;
let rounds;
let counter;
let option_blank = document.createElement("option");
let players;
let brackets;
let results;
let scores;
let losers;
let points_per_round;
let monkeys;
let bots;
let elo;
function loadResults() {
  bracketSize = Number(document.getElementById("bracket-size").innerHTML);
  rounds = Math.log2(bracketSize);
  counter = [0];
  for (let j = 0; j < rounds; j++) {
    counter[j+1] = counter[j] + bracketSize/(2**j);
  }

  // Put players in the bracket
  let promise1 = fetch("players.json").then((response)=>response.json()
  ).then(function (p){
    players = p["players"];
    elo = p["elo"];
    for (let i = 0; i < players.length; i++) {
      let id = "p" + i;
      document.getElementById(id).innerHTML = players[i];
    }
  });
  let promise2 = fetch("brackets.json").then(function(response) {
    if (response.ok) {
      response.json().then(function (response){
      brackets = response;
      })
    }
  });
  let promise3 = fetch("results.json").then(function(response) {
    if (response.ok){
      response.json().then(function(response) {
        results = response["results"];
        scores = response["scores"];
        losers = response["losers"];
      })
    } else {
      results = new Array(bracketSize-1).fill("");
      scores = new Array(bracketSize-1).fill("");
      losers = [];
    }
  })
  let promise4 = fetch("config.json").then((response)=>response.json()
  ).then(function(response) {
    points_per_round = response["points_per_round"];
  });

  Promise.all([promise1,promise2,promise3,promise4]).then(function (){ // options in each select element
    for (let i = 0; i < bracketSize/2; i++){
      let sel = document.getElementById("select"+ (counter[1] + i))
      if (players[2*i]=="Bye") { // auto select Byes
        sel.options[0].innerHTML = players[2*i+1];
        continue;
      } else if (players[2*i+1]=="Bye") {
        sel.options[0].innerHTML = players[2*i];
        continue;
      }
      let option1 = document.createElement("option");
      let option2 = document.createElement("option");
      option1.innerHTML = players[2*i];
      option2.innerHTML = players[2*i+1];
      sel.appendChild(option1)
      sel.appendChild(option2)
      if (results[counter[1]+i-bracketSize] == players[2*i]) {
        sel.value = option1.value;
      } else if (results[counter[1]+i-bracketSize] == players[2*i+1]) {
        sel.value = option2.value;
      }
      let score_text = document.getElementById("scoretext" + (counter[1] + i))
      if (score_text) {score_text.value = scores[i];}
    }

    for (let j = 2; j <= rounds; j++){
      for (let i = 0; i < bracketSize/(2**j); i++) {
        let sel = document.getElementById("select" + (counter[j] + i));
        sel.appendChild(option_blank.cloneNode(true));
        sel.appendChild(option_blank.cloneNode(true));
        sel1 = document.getElementById("select" + (counter[j-1]+2*i));
        sel2 = document.getElementById("select" + (counter[j-1]+2*i+1));
        sel.options[1].innerHTML = sel1.value;
        sel.options[2].innerHTML = sel2.value;
        if (results[counter[j]+i-bracketSize] == sel.options[1].value) {
          sel.value = sel.options[1].value;
        } else if (results[counter[j]+i-bracketSize] == sel.options[2].value) {
          sel.value = sel.options[2].value;
        }
        let score_text = document.getElementById("scoretext" + (counter[j] + i))
        if (score_text) {score_text.value = scores[counter[j]+i-bracketSize];}
      }
    }
  });
}

// The following function should update the available options depending on the choices of the user
function update_options(player){
  let round;
  let place;
  for (let j=1; j<rounds; j++) {
    if (player >= counter[j]) {
      round = j;
      break;
    }
  }
  let i = player - counter[round];
  if (i % 2) { // odd
    playerNew = counter[round+1] + (i-1)/2;
    place = 2;
  } else {
    playerNew = counter[round+1] + i/2;
    place = 1;
  }
  let sel = document.getElementById("select"+player)
  let selNew = document.getElementById("select"+playerNew)
  selNew.options[place].innerHTML = sel.value; 
}

// The following function allows the organizer to save the results of the bracket in json format
function save_results(){
  // Gather selected inputs
  for (let j = 1; j <= rounds; j++){
    for (let i = 0; i < bracketSize/(2**j); i++) {
      let sel = document.getElementById("select"+ (counter[j]+i));
      results[counter[j]+i-bracketSize] = sel.value;
      let score_text = document.getElementById("scoretext"+ (counter[j]+i));
      if (score_text) scores[counter[j]+i-bracketSize] = score_text.value;
    }
  }

  // Gather losers
  losers = [];
  for (let i = 0; i < bracketSize/2; i++) {
    if (results[i] != "") {
      if (results[i] == players[2*i] && players[2*i+1]!="Bye") {
        losers.push(players[2*i+1])
      } else if (results[i] == players[2*i+1] && players[2*i]!="Bye") {
        losers.push(players[2*i])
      }
    }
  }
  for (let j = 2; j <= rounds; j++){
    for (let i = 0; i < bracketSize/(2**j); i++) {
      if (results[counter[j]+i-bracketSize] != "") {
        if (results[counter[j]+i-bracketSize] == results[counter[j-1]+2*i-bracketSize]) {
          losers.push(results[counter[j-1]+2*i+1-bracketSize])
        } else if (results[counter[j]+i-bracketSize] == results[counter[j-1]+2*i+1-bracketSize]) {
          losers.push(results[counter[j-1]+2*i-bracketSize])
        }
      }
    }
  }

  // Define the object that contains the standings
  let table_results = {user: [],points: [],potential: [], position: [], rank: [], monkey_rank: [], bot_rank: []};
  // compute points and positions for all participants
  let entries = [];
  for (let key in brackets) {
    let points = computePoints(brackets[key],results,players,counter,points_per_round);
    entries.push({user: key, points: points,position: 1,rank: ""});
  }
  entries.sort(function(a,b) {
    return b.points - a.points;
  });
  let nr_users = entries.length;
  for (let i=1;i<nr_users;i++) {
    if (entries[i].points == entries[i-1].points) {
      entries[i].position = entries[i-1].position;
    } else {
      entries[i].position = i + 1;
    }
  }

  // compute rank
  for (let i=0;i<nr_users;i++) {
    if (entries[i].position <= Math.ceil(nr_users/2)) {
      entries[i].rank = "top " + Math.round((entries[i].position-1/2)/nr_users*100) + "%";
    } else {
      entries[i].rank = "bot " + Math.round((nr_users - entries[i].position + 1/2)/nr_users*100) + "%";
    }
    table_results.user.push(entries[i].user);
    table_results.points.push(entries[i].points);
    table_results.position.push(entries[i].position);
    table_results.rank.push(entries[i].rank);
  }

  // compute potential points
  for (let i=0;i<nr_users;i++) {
    let potential = computePotential(brackets[table_results.user[i]],results,losers,players,counter,points_per_round);
    table_results.potential.push(potential);
  }

  // Compute rank among monkeys
  generateMonkeys(10000);
  let monkey_points = [];
  for (let key in monkeys) {
    monkey_points.push(computePoints(monkeys[key],results,players,counter,points_per_round));
  }
  monkey_points.sort(function(a,b) {
    return b - a;
  })
  for (let i=0;i<nr_users;i++) {
    if (table_results.points[i] < monkey_points[monkey_points.length-1]) {
      table_results.monkey_rank.push(100);
      continue;
    }
    for (let j=0; j<monkey_points.length; j++) {
      if (table_results.points[i] >= monkey_points[j]) {
        table_results.monkey_rank.push(Math.round(j/monkey_points.length*100));
        break;
      }
    }
  }

  // Compute rank among bots
  generateBots(10000);
  let bot_points = [];
  for (let key in bots) {
    bot_points.push(computePoints(bots[key],results,players,counter,points_per_round));
  }
  bot_points.sort(function(a,b) {
    return b - a;
  })
  for (let i=0;i<nr_users;i++) {
    if (table_results.points[i] < bot_points[bot_points.length-1]) {
      table_results.bot_rank.push(100);
      continue;
    }
    for (let j=0; j<bot_points.length; j++) {
      if (table_results.points[i] >= bot_points[j]) {
        table_results.bot_rank.push(Math.round(j/bot_points.length*100));
        break;
      }
    }
  }

  let blob = new Blob([JSON.stringify({results: results,scores: scores,losers: losers,table_results: table_results})],{type : "application:json"});
  url = URL.createObjectURL(blob);
  let link = document.createElement('a');
  link.href = url;
  link.setAttribute("download","results.json");
  link.click();
}

function generateMonkeys(number_monkeys) {
  monkeys = {};
  for (let k=0; k<number_monkeys; k++){
    let bracket=[];
    // Picks for the second round
    for (let i = 0; i < bracketSize/2; i++){
      if (players[2*i]=="Bye") {
        bracket.push(players[2*i+1]);
      } else if (players[2*i+1]=="Bye") {
        bracket.push(players[2*i]);
      } else if (Math.random()<0.5) {
        bracket.push(players[2*i]);
      } else {
        bracket.push(players[2*i+1]);
      }
    }
    // picks for the third round onwards
    for (let j = 1; j < rounds; j++){
      for (let i = 0; i < bracketSize/(2**(j+1)); i++) {
        if (Math.random()<0.5) {
          bracket.push(bracket[counter[j]-bracketSize+2*i]);
        } else {
          bracket.push(bracket[counter[j]-bracketSize+2*i+1]);
        }
      }
    }
    // Save bracket to monkeys
    monkeys["monkey"+k] = bracket;
  }
}

function generateBots(number_bots) {
  bots = {};
  for (let k=0; k<number_bots; k++){
    let bracket=[];
    let bracket_elo = [];
    // Picks for the second round
    for (let i = 0; i < bracketSize/2; i++){
      if (players[2*i]=="Bye") {
        bracket.push(players[2*i+1]);
        bracket_elo.push(elo[2*i+1]);
        continue;
      } else if (players[2*i+1]=="Bye") {
        bracket.push(players[2*i]);
        bracket_elo.push(elo[2*i]);
        continue
      }
      let Q1 = 10**(elo[2*i]/400);
      let Q2 = 10**(elo[2*i+1]/400);
      let probability = Q1/(Q1+Q2);
      if (Math.random()<probability) {
        bracket.push(players[2*i]);
        bracket_elo.push(elo[2*i])
      } else {
        bracket.push(players[2*i+1]);
        bracket_elo.push(elo[2*i+1]);
      } 
    }
    // picks for the third round onwards
    for (let j = 1; j < rounds; j++){
      for (let i = 0; i < bracketSize/(2**(j+1)); i++) {
        let Q1 = 10**(bracket_elo[counter[j]-bracketSize+2*i]/400);
        let Q2 = 10**(bracket_elo[counter[j]-bracketSize+2*i+1]/400);
        let probability = Q1/(Q1+Q2);
        if (Math.random()<probability) {
          bracket.push(bracket[counter[j]-bracketSize+2*i]);
          bracket_elo.push(bracket_elo[counter[j]-bracketSize+2*i]);
        } else {
          bracket.push(bracket[counter[j]-bracketSize+2*i+1]);
          bracket_elo.push(bracket_elo[counter[j]-bracketSize+2*i+1]);
        }
      }
    }
    // Save bracket to bots
    bots["bot"+k] = bracket;
  }
}

function generateElo() {
  let bracket=[];
  let bracket_elo = [];
  // Picks for the second round
  for (let i = 0; i < bracketSize/2; i++){
    if (players[2*i]=="Bye") {
      bracket.push(players[2*i+1]);
      bracket_elo.push(elo[2*i+1]);
      continue;
    } else if (players[2*i+1]=="Bye") {
      bracket.push(players[2*i]);
      bracket_elo.push(elo[2*i]);
      continue
    }
    if (elo[2*i]>elo[2*i+1]) {
      bracket.push(players[2*i]);
      bracket_elo.push(elo[2*i])
    } else {
      bracket.push(players[2*i+1]);
      bracket_elo.push(elo[2*i+1]);
    } 
  }
  // picks for the third round onwards
  for (let j = 1; j < rounds; j++){
    for (let i = 0; i < bracketSize/(2**(j+1)); i++) {
      if (bracket_elo[counter[j]-bracketSize+2*i]>bracket_elo[counter[j]-bracketSize+2*i+1]) {
        bracket.push(bracket[counter[j]-bracketSize+2*i]);
        bracket_elo.push(bracket_elo[counter[j]-bracketSize+2*i]);
      } else {
        bracket.push(bracket[counter[j]-bracketSize+2*i+1]);
        bracket_elo.push(bracket_elo[counter[j]-bracketSize+2*i+1]);
      }
    }
  }

  let blob = new Blob([JSON.stringify({Elo: bracket})],{type : "application:json"});
  url = URL.createObjectURL(blob);
  link = document.createElement('a');
  link.href = url;
  link.setAttribute("download","Elo.json");
  link.click();
}