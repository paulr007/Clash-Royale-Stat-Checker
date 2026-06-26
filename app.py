from flask import Flask, render_template, request
import requests
from config import API_KEY

app = Flask(__name__)

API_KEY = API_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stats")
def stats():
    tag = request.args.get("tag").replace("#", "%23")

    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(
        f"https://api.clashroyale.com/v1/players/{tag}/battlelog",
        headers=headers,
    )

    battles = response.json()

    wins = 0
    losses = 0
    for battle in battles:
        if battle["team"][0]["crowns"] > battle["opponent"][0]["crowns"]:
            wins += 1
        else:
            losses += 1

    winrate = round(wins / (wins + losses) * 100, 1)

    deck = []

    response_player = requests.get(
        f"https://api.clashroyale.com/v1/players/{tag}", headers=headers
    )
    player = response_player.json()

    for card in player["currentDeck"]:
        appendings = {
            "name": card["name"],
        }
        if card.get("evolutionLevel") == 2 and "heroMedium" in card["iconUrls"]:
            appendings["image"] = card["iconUrls"]["heroMedium"]
        elif card.get("evolutionLevel") == 1 and "evolutionMedium" in card["iconUrls"]:
            appendings["image"] = card["iconUrls"]["evolutionMedium"]
        else:
            appendings["image"] = card["iconUrls"]["medium"]
        deck.append(appendings)

    return render_template(
        "stats.html",
        wins=wins,
        losses=losses,
        winrate=winrate,
        deck=deck,
        tag=request.args.get("tag"),
    )


@app.route("/battlelog")
def log():
    tag = request.args.get("tag").replace("#", "%23")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    battle_log = requests.get(
        f"https://api.clashroyale.com/v1/players/{tag}/battlelog",
        headers=headers,
    )
    battles = battle_log.json()
    opponents = []
    for battle in battles:
        current_opponent = battle["opponent"][0]
        if current_opponent["name"] == "Morais":
            print(current_opponent)
        deck = []
        for card in current_opponent["cards"]:
            appendings = {
                "name": card["name"],
            }
            if card.get("evolutionLevel") == 2 and "heroMedium" in card["iconUrls"]:
                appendings["image"] = card["iconUrls"]["heroMedium"]
            elif (
                card.get("evolutionLevel") == 1
                and "evolutionMedium" in card["iconUrls"]
            ):
                appendings["image"] = card["iconUrls"]["evolutionMedium"]
            else:
                appendings["image"] = card["iconUrls"]["medium"]
            deck.append(appendings)
        opponents.append({"name": current_opponent["name"], "deck": deck})
    return render_template(
        "battlelog.html", opponents=opponents, tag=request.args.get("tag")
    )


if __name__ == "__main__":
    app.run(debug=True)
