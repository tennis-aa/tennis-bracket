let x = Number(document.querySelectorAll(".player:last-child")[0].id.replace("p",""))+1;
let bracketSize = (x+1)/2;
let rounds = Math.log2(bracketSize);
let counter = [0];
for (let j = 0; j < rounds; j++) {
  counter[j+1] = counter[j] + bracketSize/(2**j);
}

let options = []
let option_blank = document.createElement("option");
// option_blank.innerHTML = " ";
option_blank.setAttribute("value","");
let players;

// sleep for three seconds
// console.log("now")
// let now = Date.now();
// let end = now + 3000;
// while (now<end) {
//   now = Date.now();
// }
// console.log("end")


// Put players in the bracket
fetch("players.json").then((response)=>response.json()
).then(function (p){
  console.log("start");
  players = p;
  for (let i = 0; i < p.length; i++) {
    let id = "p" + i;
    document.getElementById(id).innerHTML = p[i];
  }
}).then(function (){ // Put select elements to pick winners
  for (let i = 0; i < bracketSize; i++){
      let option = document.createElement("option");
      option.innerHTML = players[i];
      options.push(option);
  }
  for (let j = 1; j <= rounds; j++){
    for (let i = 0; i < bracketSize/(2**j); i++) {
      let selectNode = document.createElement("select");
      // selectNode.setAttribute("onchange","update_options()");
      selectNode.setAttribute("id","select"+ (counter[j] + i));
      selectNode.appendChild(option_blank.cloneNode(true));
      let predecessors = [...Array(2**j).keys()].map(x => x + i*(2**j));
      for (let k=0; k<predecessors.length;k++) {
        selectNode.appendChild(options[predecessors[k]].cloneNode(true));
      }
      let id = "p" + (counter[j] + i);
      let pl = document.getElementById(id);
      pl.appendChild(selectNode);
    }
  }
});


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
  link.innerText = 'Open the URL';
  link.setAttribute("download","bracket.json");
  link.click();
}