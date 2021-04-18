let bracketSize;
let rounds;
let counter;
let option_blank = document.createElement("option");
let players;
let brackets;
let results;
let points_per_round

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
    players = p;
    for (let i = 0; i < p.length; i++) {
      let id = "p" + i;
      document.getElementById(id).innerHTML = p[i];
    }
  });
  let promise2 = fetch("brackets.json").then((response)=>response.json()
  ).then(function (response){
    brackets = response;
  });
  let promise3 = fetch("results.json").then((response)=>response.json()
  ).then(function(response){
    results = response;
  })
  promise4 = fetch("config.json").then((response)=>response.json()
  ).then(function(response) {
    points_per_round = response["points_per_round"];
  });


  Promise.all([promise1,promise2,promise3,promise4]).then(function (){ // options in each select element
    for (let i = 0; i < bracketSize/2; i++){
      let sel = document.getElementById("select"+ (counter[1] + i))
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
  console.log(playerNew)
  let sel = document.getElementById("select"+player)
  let selNew = document.getElementById("select"+playerNew)
  selNew.options[place].innerHTML = sel.value; 
  // for (let j = 1; j <= rounds-1; j++){
  //   for (let i = 0; i < bracketSize/(2**j); i++) {
  //     let selectNode = document.getElementById("select"+ (counter[j]+i));
  //     let selectchildNodes = selectNode.childNodes;
  //     len = selectchildNodes.length;
  //     for (let k=0; k<len;k++){
  //       selectNode.removeChild(selectchildNodes[0]);
  //     }
  //   }
  // }
}

// The following function allows the user to save the bracket in json format
function save_results(){
  // Gather selected inputs
  for (let j = 1; j <= rounds; j++){
    for (let i = 0; i < bracketSize/(2**j); i++) {
      let sel = document.getElementById("select"+ (counter[j]+i));
      results[i] = sel.value;
    }
  }

  // compute points and positions for all participants
  let entries = [];
  let table_results = {user: [],points: [], position: [], rank: []}
  for (let key in brackets) {
    let points = computePoints(brackets[key],results,points_per_round);
    entries.push({user: key, points: points,position: 1,rank: ""});
  }
  entries.sort(function(a,b) {
    return b.points - a.points;
  });
  let nr_users = entries.length;
  for (let i=1;i<nr_users;i++) {
    if (entries[i].points == entries[i-1].points) {
      entries[i].position = entries[i-1].position
    } else {
      entries[i].position = i + 1;
    }
  }
  // compute rank
  for (let i=0;i<nr_users;i++) {
    if (entries[i].position <= nr_users/2) {
      entries[i].rank = "top " + (entries[i].position/nr_users*100) + "%";
    } else {
      entries[i].rank = "bot " + ((nr_users - entries[i].position + 1)/nr_users*100) + "%";
    }
    table_results.user.push(entries[i].user)
    table_results.points.push(entries[i].points)
    table_results.position.push(entries[i].position)
    table_results.rank.push(entries[i].rank)
  }
  console.log(table_results)


  let blob = new Blob([JSON.stringify(results)],{type : "application:json"});
  url = URL.createObjectURL(blob);
  let link = document.createElement('a');
  link.href = url;
  link.setAttribute("download","results.json");
  link.click();

  blob = new Blob([JSON.stringify(table_results)],{type : "application:json"});
  url = URL.createObjectURL(blob);
  link = document.createElement('a');
  link.href = url;
  link.setAttribute("download","table_results.json");
  link.click();
}