var dealerSum = 0;
var yourSum = 0;

var dealerAceCount = 0;
var yourAceCount = 0; 

var bet = 0;

var hidden;
var deck;

var canHit = true; //allows the player (you) to draw while yourSum <= 21

window.onload = function() {
    startGame();
}

async function getJSON(url) {
    json = await (await fetch(url)).json();
    return json
}

function buildDeck() {
    let values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
    let types = ["C", "D", "H", "S"];
    deck = [];

    for (let i = 0; i < types.length; i++) {
        for (let j = 0; j < values.length; j++) {
            deck.push(values[j] + "-" + types[i]); //A-C -> K-C, A-D -> K-D
        }
    }
    // console.log(deck);
}

function httpGet(urlIn) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", urlIn);
}

function startGame() {
    httpGet("http://127.0.0.1:5000/game_dealer/start_game");
    while (true) {
        httpGet()
    }
    const data = getJSON("http://127.0.0.1:5000/game_dealer/table"); 
    console.log(data);
    // hidden = deck.pop();
    // dealerSum += getValue(hidden);
    // dealerAceCount += checkAce(hidden);
    // // console.log(hidden);
    // // console.log(dealerSum);
    // while (dealerSum < 17) {
    //     //<img src="./cards/4-C.png">
    //     let cardImg = document.createElement("img");
    //     let card = deck.pop();
    //     cardImg.src = "game\\static\\cards\\" + card + ".png";
    //     dealerSum += getValue(card);
    //     dealerAceCount += checkAce(card);
    //     document.getElementById("dealer-cards").append(cardImg);
    // }
    // console.log(dealerSum);

    // for (let i = 0; i < 2; i++) {
    //     let cardImg = document.createElement("img");
    //     let card = deck.pop();
    //     cardImg.src = "game\\static\\cards\\" + card + ".png";
    //     yourSum += getValue(card);
    //     yourAceCount += checkAce(card);
    //     document.getElementById("your-cards").append(cardImg);
    // }

    // console.log(yourSum);
    // document.getElementById("hit").addEventListener("click", hit);
    // document.getElementById("stay").addEventListener("click", stay);
    // document.getElementById("bet5").addEventListener("click", bet5);
    // document.getElementById("bet10").addEventListener("click", bet10);
    // document.getElementById("bet20").addEventListener("click", bet20);
    // document.getElementById("bet50").addEventListener("click", bet50);
    // document.getElementById("bet100").addEventListener("click", bet100);

    // document.getElementById("current-bet").innerText = bet;

}

function hit() {
    if (!canHit) {
        return;
    }

    let cardImg = document.createElement("img");
    let card = deck.pop();
    cardImg.src = "game\\static\\cards\\" + card + ".png";
    yourSum += getValue(card);
    yourAceCount += checkAce(card);
    document.getElementById("your-cards").append(cardImg);

    if (reduceAce(yourSum, yourAceCount) > 21) { //A, J, 8 -> 1 + 10 + 8
        canHit = false;
    }

}

async function stay() {
    dealerSum = reduceAce(dealerSum, dealerAceCount);
    yourSum = reduceAce(yourSum, yourAceCount);

    canHit = false;
    document.getElementById("hidden").src = "game\\static\\cards\\" + hidden + ".png";

    let message = "";
    if (yourSum > 21) {
        message = "You Lose!";
    }
    else if (dealerSum > 21) {
        message = "You win!";
    }
    //both you and dealer <= 21
    else if (yourSum == dealerSum) {
        message = "Tie!";
    }
    else if (yourSum > dealerSum) {
        message = "You Win!";
    }
    else if (yourSum < dealerSum) {
        message = "You Lose!";
    }
    card = await getJSON("http://127.0.0.1:5000/game_dealer/card");
    card = "COLOR: " + card.color + ' VALUE: ' + card.value + ' SIGN: ' + card.sign;
    document.getElementById("dealer-sum").innerText = dealerSum;
    document.getElementById("your-sum").innerText = yourSum;
    document.getElementById("results").innerText = card
}

function bet5() {
    bet += 5;
    document.getElementById("current-bet").innerText = bet;
}
function bet10() {
    bet += 10;
    document.getElementById("current-bet").innerText = bet;
}
function bet20() {
    bet += 20;
    document.getElementById("current-bet").innerText = bet;
}
function bet50() {
    bet += 50;
    document.getElementById("current-bet").innerText = bet;
}
function bet100() {
    bet += 100;
    document.getElementById("current-bet").innerText = bet;
}

function getValue(card) {
    let data = card.split("-"); // "4-C" -> ["4", "C"]
    let value = data[0];

    if (isNaN(value)) { //A J Q K
        if (value == "A") {
            return 11;
        }
        return 10;
    }
    return parseInt(value);
}

function checkAce(card) {
    if (card[0] == "A") {
        return 1;
    }
    return 0;
}

function reduceAce(playerSum, playerAceCount) {
    while (playerSum > 21 && playerAceCount > 0) {
        playerSum -= 10;
        playerAceCount -= 1;
    }
    return playerSum;
}
