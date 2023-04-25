import json
import requests
import tkinter as tk

with open("mykey.txt", "r") as f:
    mykey = f.read().rstrip("\n")

baseUrl = "https://api.clashroyale.com/v1"
endpoint = "/clans/%232G0QP2RU/riverracelog?limit=100"

headers = {
    'Authorization': f'Bearer: {mykey}',
}

response = requests.get(baseUrl + endpoint, headers=headers)
print(response.text)
data = json.loads(response.text)

# Select the season to analyze
selectedSeason = max(entry["seasonId"] for entry in data["items"])

# Select the section to analyze
selectedSection = max(entry["sectionIndex"] for entry in data["items"] if entry["seasonId"] == selectedSeason)

# Extract the list of participants and their fame points for Viva Vodka clan in sectionIndex 3
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
    if standing["clan"]["name"] == "Viva Vodka"
    for participant in standing["clan"]["participants"]
]

# Sort the participants by fame points
participants = sorted(participants, key=lambda p: p["fame"], reverse=True)

# Create a window
window = tk.Tk()
window.title("Clash Royale Participants")
window.geometry("600x400")

# Create a listbox to display the participants
listbox = tk.Listbox(window, width=70, height=20)
listbox.pack(pady=10)

# Add each participant to the listbox, with color-coded text
for participant in participants:
    color = "green"  # default color is green
    if participant["fame"] > 3000:
        color = "blue"  # blue color
    elif participant["fame"] < 1600:
        color = "red"  # red color
    elif participant["boatAttacks"] > 0:
        color = "orange"  # orange color
    text = f"Name: {participant['name']}, Tag: {participant['tag']}, Fame Points: {participant['fame']}, Boat Attacks: {participant['boatAttacks']}"
    listbox.insert(tk.END, text)
    listbox.itemconfig(tk.END, fg=color)

# Add a label to display the total number of participants
total_label = tk.Label(window, text=f"Total participants: {len(participants)}")
total_label.pack()

# Start the event loop
window.mainloop()



