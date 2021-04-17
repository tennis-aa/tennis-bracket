let bracketSize;
let rounds;
let counter;
let options;
let option_blank;
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

  options = []
  option_blank = document.createElement("option");
  // option_blank.innerHTML = " ";
  option_blank.setAttribute("value","");


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
    for (let i = 0; i < bracketSize; i++){
        let option = document.createElement("option");
        option.innerHTML = players[i];
        options.push(option);
    }
    for (let j = 1; j <= rounds; j++){
      for (let i = 0; i < bracketSize/(2**j); i++) {
        let selectNode = document.getElementById("select"+ (counter[j] + i))
        document.createElement("select");
        let predecessors = [...Array(2**j).keys()].map(x => x + i*(2**j));
        for (let k=0; k<predecessors.length;k++) {
          selectNode.appendChild(options[predecessors[k]].cloneNode(true));
          if (results[counter[j]+i-bracketSize] == options[predecessors[k]].value) {
            selectNode.value = options[predecessors[k]].value;
          }
        }
      }
    }
  });
}

// The following function should update the available options depending on the choices of the user
function update_options(){
  for (let j = 1; j <= rounds-1; j++){
    for (let i = 0; i < bracketSize/(2**j); i++) {
      let selectNode = document.getElementById("select"+ (counter[j]+i));
      let selectchildNodes = selectNode.childNodes;
      len = selectchildNodes.length;
      for (let k=0; k<len;k++){
        selectNode.removeChild(selectchildNodes[0]);
      }
      // selectNode.appendChild(option_blank.cloneNode(true));
      // let predecessors = [...Array(2**j).keys()].map(x => x + i*(2**j));
      // for (let k=0; k<predecessors.length;k++) {
      //   selectNode.appendChild(options[predecessors[k]].cloneNode(true));
      // }
    }
  }
}

// The following function allows the user to save the bracket in json format
function save_results(){
  // Gather selected inputs
  for (let j = 1; j <= rounds; j++){
    for (let i = 0; i < bracketSize/(2**j); i++) {
      let selectNode = document.getElementById("select"+ (counter[j]+i));
      results[i] = selectNode.value;
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