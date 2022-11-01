var bet = 0;
var data = 0;
var frontend = {};

window.onload = function() {
    startGame();
}

async function getJSON(url) {
    json = await (await fetch(url)).json();
    return json
}

async function httpGet(urlIn) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", urlIn);
}

async function httpPost(urlIn) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", urlIn)
}

async function hit() {
    frontend = await getJSON("http://127.0.0.1:5000/game_dealer/table_hit");
    await updateFrontend()
    switch (frontend["result"]) {
        case -1:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "You Lose";
            break;
        case 1:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "Tie";
            break;
        case 2:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "You win";
            break;
        case "None":
            break;
    }
}

async function stay() {
    frontend = await getJSON("http://127.0.0.1:5000/game_dealer/table_stay");
    await updateFrontend()
    console.log(frontend["result"])
    switch (frontend["result"]) {
        case -1:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "You Lose";
            break;
        case 1:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "Tie";
            break;
        case 2:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "You win";
            break;
        default:
            await proxy_stay()
            break;
    }
    document.getElementById("hit").removeEventListener("click", hit); // addEventListener("click", hit);
}

async function proxy_stay() {
    frontend = await getJSON("http://127.0.0.1:5000/game_dealer/table_stay");
    await updateFrontend()
    console.log(frontend["result"])
    switch (frontend["result"]) {
        case -1:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "You Lose";
            break;
        case 1:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "Tie";
            break;
        case 2:
            fillHandOponent(frontend["oponent"]["cards"], 0);
            document.getElementById("results").innerText = "You win";
            break;
        default:
            await proxy_stay()
            break;
    }
}

function exit() {
    window.location.replace("http://127.0.0.1:5000/exit");
}

function fillHandOponent(cards, hidden=1) {
    elem = document.getElementById("oponent");
    while(elem.firstChild)
    {
        elem.removeChild(elem.firstChild);
    }

    cards.forEach(
        (card, index) =>{
            let cardImg = document.createElement("img");
            if (hidden == 1){
                if (index >= 1){
                    cardImg.src = "game\\static\\cards\\" + Object.keys(card)[0] + ".png";
                } else {
                    cardImg.src = "\\game\\static\\cards_by_ola\\tyl.png";
                }
            } else {
                cardImg.src = "game\\static\\cards\\" + Object.keys(card)[0] + ".png";
            }
            document.getElementById("oponent").append(cardImg);
        }
    )
}

function fillHandPlayer(cards) {
    elem = document.getElementById("player");
    while(elem.firstChild)
    {
        elem.removeChild(elem.firstChild);
    }
    cards.forEach(
        (card) => {
            let cardImg = document.createElement("img");
            cardImg.src = "game\\static\\cards\\"+Object.keys(card)[0]+".png";
            document.getElementById("player").append(cardImg);
        }
    )
}

async function updateFrontend() {
    console.log(frontend)
    fillHandOponent(frontend["oponent"]["cards"]);
    fillHandPlayer(frontend["player"]["cards"]);
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

async function startGame() {
    document.getElementById("exit").addEventListener("click", exit);
    document.getElementById("bet5").addEventListener("click", bet5);
    document.getElementById("bet10").addEventListener("click", bet10);
    document.getElementById("bet20").addEventListener("click", bet20);
    document.getElementById("bet50").addEventListener("click", bet50);
    document.getElementById("bet100").addEventListener("click", bet100);
    document.getElementById("hit").addEventListener("click", hit);
    document.getElementById("stay").addEventListener("click", stay);

    frontend = await getJSON("http://127.0.0.1:5000/game_dealer/table");
    await updateFrontend();
}
