// This function computes the number of points scored by bracket given results and 
// an array of points_per_round
function computePoints(bracket,results,players,points_per_round) {
    let bracketSize = bracket.length + 1;
    let rounds = Math.log2(bracketSize);
    let points = 0;
    let counter = [0];
    for (let j = 0; j < rounds; j++) {
        counter[j+1] = counter[j] + bracketSize/(2**j);
    }
    let round = 0;
    for (let i = 0; i < bracket.length; i++) {
        if (i+bracketSize >= counter[round+2]) {round += 1;}
        if (bracket[i] == results[i] && results[i] != ""){
            points += points_per_round[round];
        }
    }
    for (let i=0; i<players.length; i++) { // reove points from byes
        if (players[i]=="Bye") {
            points -= points_per_round[0];
        }
    }
    return points;
}

// Debug block
// points_per_round = [1,2,3];
// bracket1 = ["pl1","pl3","pl5","pl7","pl1","pl5","pl1"];
// bracket2 = ["pl2","pl4","pl6","pl8","pl4","pl8","pl8"];
// results = ["pl1","pl3","pl5","pl7","pl1","pl5","pl1"];

// computePoints(bracket1,results,points_per_round);
// computePoints(bracket2,results,points_per_round);