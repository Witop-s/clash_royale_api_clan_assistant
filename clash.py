import json
import requests
import webbrowser

with open("mykey2.txt", "r") as f:
    mykey = f.read().strip()

with open("infos.txt", "r") as f:
    lines = f.readlines()

clan_tag = lines[0].strip().split("=")[1]
over_value_highlight = int(lines[1].strip().split("=")[1])
under_value_highlight = int(lines[2].strip().split("=")[1])

# Convert the clan tag to a proper format
if clan_tag.startswith("#"):
    formated_clan_tag = clan_tag[1:]
formated_clan_tag = "%23" + formated_clan_tag.upper()

baseUrl = "https://api.clashroyale.com/v1"
headers = {
    "Authorization": f"Bearer: {mykey}"
}

# Get river race data
endpoint = "/clans/" + formated_clan_tag + "/riverracelog?limit=100"
response = requests.get(baseUrl + endpoint, headers=headers)
data = response.json()

# Select the season to analyze
selectedSeason = max(entry["seasonId"] for entry in data["items"])

# Select the section to analyze
selectedSection = max(entry["sectionIndex"] for entry in data["items"] if entry["seasonId"] == selectedSeason)

# Extract the list of participants and their fame points for the given clan
participants = [
    {
        "name": participant["name"],
        "tag": participant["tag"],
        "fame": participant["fame"],
        "boatAttacks": participant["boatAttacks"]
    }
    for entry in data["items"]
    if entry["seasonId"] == selectedSeason and entry["sectionIndex"] == selectedSection
    for standing in entry["standings"]
    if standing["clan"]["tag"] == clan_tag
    for participant in standing["clan"]["participants"]
]

# Sort the participants by fame points
participants.sort(key=lambda p: p["fame"], reverse=True)


# Print the list of participants and their fame points
'''
for i, participant in enumerate(participants):
    color = "\033[0m"  # default color is green
    if participant["fame"] > over_value_highlight:
        color = "\033[94m" # blue color
    elif participant["fame"] < under_value_highlight:
        color = "\033[91m"  # red color
    elif participant["boatAttacks"] > 0:
        color = "\033[33m"  # orange color
    print(f"{color}Name: {participant['name']}, Tag: {participant['tag']}, Fame Points: {participant['fame']}, Boat Attacks: {participant['boatAttacks']}\033[0m")

print(f"Total participants: {len(participants)}")
'''


# Get member data
endpoint = "/clans/" + formated_clan_tag + "/members"
response = requests.get(baseUrl + endpoint, headers=headers)
data = response.json()

# Extract the list of players and their tag
players = [{"name": player["name"], "tag": player["tag"], "role": player["role"]} for player in data["items"]]

#print(f"Total players: {len(players)}")

unactivePlayers = []
players_set = set(player["tag"] for player in players)
participants_set = set(participant["tag"] for participant in participants if participant["fame"] < under_value_highlight)
tags_set = players_set.intersection(participants_set)

for participant in participants:
    if participant["tag"] in tags_set:
        player = next((p for p in players if p["tag"] == participant["tag"]), None)
        if player:
            unactivePlayers.append({
                "name": player["name"],
                "tag": player["tag"],
                "fame": participant["fame"],
                "boatAttacks": participant["boatAttacks"]
            })

unactivePlayers = sorted(unactivePlayers, key=lambda p: p["fame"], reverse=True)

# Print the list of unactive players
print("------------------ Active Players ------------------")
print(f"Total unactive players: {len(unactivePlayers)}")
for i, player in enumerate(unactivePlayers):
    print(f"Name: {player['name']}, Tag: {player['tag']}, Fame Points: {player['fame']}, Boat Attacks: {player['boatAttacks']}")
    #open a new tab in browser for each player, but without the '#' in the tag
    webbrowser.open_new_tab(f"https://royaleapi.com/player/{player['tag'][1:]}")

promotionList = []
for i, player in enumerate(participants):
    if player["fame"] > over_value_highlight:
        promotionList.append(player)

# Print the list of players to promote
print("------------------ Promotion List ------------------")
print(f"Total players to promote: {len(promotionList)}")
for i, player in enumerate(promotionList):
    print(f"Name: {player['name']}, Fame Points: {player['fame']}")