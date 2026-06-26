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
        f"https://api.clashroyale.com/v1/players/{tag}/battlelog", headers=headers
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
        deck.append({"name": card["name"], "image": card["iconUrls"]["medium"]})

    return render_template(
        "stats.html", wins=wins, losses=losses, winrate=winrate, deck=deck
    )


if __name__ == "__main__":
    app.run(debug=True)
