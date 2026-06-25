import requests
import json
from config import API_KEY, PLAYER_TAG

API_KEY = API_KEY
PLAYER_TAG = PLAYER_TAG

headers = {"Authorization": f"Bearer {API_KEY}"}

tag = PLAYER_TAG.replace("#", "%23")

battle_response = requests.get(
    f"https://api.clashroyale.com/v1/players/{tag}/battlelog", headers=headers
)

with open("cardWinRelation.json", "w") as f:
    battles = battle_response.json()
    my_card_wins = {}
    my_card_games = {}
    opp_card_losses = {}
    opp_card_games = {}
    for battle in battles:
        for card in battle["team"][0]["cards"]:
            if card["name"] not in my_card_wins:
                my_card_wins[card["name"]] = 0
                my_card_games[card["name"]] = 0
            my_card_games[card["name"]] += 1
        for card in battle["opponent"][0]["cards"]:
            if card["name"] not in opp_card_losses:
                opp_card_losses[card["name"]] = 0
                opp_card_games[card["name"]] = 0
            opp_card_games[card["name"]] += 1
        my_crowns = battle["team"][0]["crowns"]
        opp_crowns = battle["opponent"][0]["crowns"]
        if my_crowns > opp_crowns:
            for card in battle["team"][0]["cards"]:
                my_card_wins[card["name"]] += 1
        else:
            for card in battle["opponent"][0]["cards"]:
                opp_card_losses[card["name"]] += 1
    card_winrate = {}
    for name in my_card_wins:
        card_winrate[name] = {
            "Winrate": round(my_card_wins[name] / my_card_games[name] * 100, 1),
            "Wins": my_card_wins[name],
            "Losses": my_card_games[name] - my_card_wins[name],
            "Games": my_card_games[name],
        }
    card_lossrate = {}
    for name in opp_card_losses:
        card_lossrate[name] = {
            "Lossrate": round(opp_card_losses[name] / opp_card_games[name] * 100, 1),
            "Losses": opp_card_losses[name],
            "Games": opp_card_games[name],
        }

    card_winrate_sorted = dict(
        sorted(card_winrate.items(), key=lambda x: x[1]["Winrate"], reverse=True)
    )
    card_lossrate_sorted = dict(
        sorted(card_lossrate.items(), key=lambda x: x[1]["Lossrate"], reverse=True)
    )
    json.dump(
        {"my_win_stats": card_winrate_sorted, "my_loss_cards": card_lossrate_sorted},
        f,
        indent=4,
    )
