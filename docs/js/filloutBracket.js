let bracketSize;
let rounds;
let counter;
let option_blank = document.createElement("option");
let players;
function loadFillout() {
  bracketSize = Number(document.getElementById("bracket-size").innerHTML);
  rounds = Math.log2(bracketSize);
  counter = [0];
  for (let j = 0; j < rounds; j++) {
    counter[j+1] = counter[j] + bracketSize/(2**j);
  }

  // Put players in the bracket
  fetch("./players.json").then((response)=>response.json()
  ).then(function (p){
    players = p["players"];
    for (let i = 0; i < players.length; i++) {
      let id = "p" + i;
      document.getElementById(id).innerHTML = players[i];
    }
  }).then(function (){ // Put select elements to pick winners in the first round
    for (let i = 0; i < bracketSize/2; i++){
      let sel = document.getElementById("select"+ (counter[1] + i));
      let option1 = document.createElement("option");
      let option2 = document.createElement("option");
      option1.innerHTML = players[2*i];
      option2.innerHTML = players[2*i+1];
      sel.appendChild(option1)
      sel.appendChild(option2)
    } // Put select elements to pick winners in other rounds
    for (let j=2; j<=rounds; j++) {
      for (let i=0; i<bracketSize/(2**j); i++) {
        let sel = document.getElementById("select"+ (counter[j] + i));
        sel.appendChild(option_blank.cloneNode(true));
        sel.appendChild(option_blank.cloneNode(true));
      }
    }
    for (let i = 0; i < bracketSize/2; i++){ // auto select byes
      let sel = document.getElementById("select"+ (counter[1] + i));
      if (players[2*i]=="Bye") {
        sel.innerHTML = "";
        let opt = document.createElement("option");
        opt.innerHTML = players[2*i+1];
        sel.appendChild(opt);
        update_options(counter[1] + i);
        continue;
      } else if (players[2*i+1]=="Bye") {
        sel.innerHTML = "";
        let opt = document.createElement("option");
        opt.innerHTML = players[2*i];
        sel.appendChild(opt);
        update_options(counter[1] + i);
        continue;
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
function save_bracket(){
  let bracket = [];
  let username = document.getElementById("user-name").value;
  for (let j = 1; j <= rounds; j++){
    for (let i = 0; i < bracketSize/(2**j); i++) {
      let selectNode = document.getElementById("select"+ (counter[j]+i));
      bracket.push(selectNode.value);
    }
  }
  let entry = {};
  entry[username] = bracket;
  let blob = new Blob([JSON.stringify(entry)],{type : "application:json"});
  url = URL.createObjectURL(blob);
  let link = document.createElement('a');
  link.href = url;
  link.setAttribute("download",username + ".json");
  link.click();
}