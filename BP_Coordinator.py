import random
import numpy as np

def num_players(m):
    while True:
        try:
            if m == 0:  # SOLO CashCup selected
                x = int(input("Enter number of players: "))
                if x <= 0:
                    print("You must enter a positive number of players.")
                elif x >= 2:
                    print(f"You have entered {x} players.")
                    return x
                else:
                    print("You need at least two players.")
            if m == 1:  # DUO CashCup selected
                x = int(input("Enter an even number of players greater or equal than four: "))
                if x <= 0:
                    print("You must enter a positive number of players.")
                elif x >= 4:
                    if x % 2 != 0:
                        print("You must enter an even number of players")
                    else:
                        print(f"You have entered {x} players.")
                        return x
                else:
                    print("You need at least four players.")
        except ValueError:
            print("Invalid input! Please enter a valid number of players.")

def names(x):
    player_names = []
    
    for i in range(x):
        while True:
            name = input(f"Enter the name of player {i + 1}: ")
            if name in player_names:
                print("Name already exists. Please choose a different name.")
            else:
                player_names.append(name)
                break
            
    if len(player_names) != x:
        print("The number of players does not match the number of names")
    else:
        print("****************PLAYERS****************")
        for i, name in enumerate(player_names):
            print(f"Player {i + 1}: {name}")
        random.shuffle(player_names)
        return player_names
def mode():
    while True:
        m = input("Choose between solo (s) or duo (d) CashCup: ")
        if m == 's':
            mode_select = 0
            return mode_select
        if m == 'd':
            mode_select = 1
            return mode_select
        else:
            print("Invalid input! Input must be 's' or 'd.")
            
def draw_teams(p):
    if len(p) % 2 != 0 or len(p)<4:
        print("The number of players is not ideal! Could not create proper teams.")
        
    random.shuffle(p)
    num_teams=len(p)//2
    teams=[]
    for i in range(num_teams):
        team=p[i*2:(i+1)*2]
        teams.append(team)
    for i, team in enumerate(teams):
        print(f"Team {i + 1}: {team}")
    return teams


def create_groupstage(arr):
    n = len(arr)
    if n <= 5:
        # Wenn die Liste klein genug ist, gib einzelne Gruppe zurück
        return [arr]

    num_groups = (n + 4) // 5  # Berechne Anzahl der Gruppen
    group_size = (n + num_groups - 1) // num_groups  # durchschnittliche Gruppengröße.

    # Erstelle leere Gruppen.
    groups = [[] for _ in range(num_groups)]

    # Fülle die Gruppen gleichmäßig
    for i, item in enumerate(arr):
        group_index = i // group_size
        groups[group_index].append(item)

    # falls Gruppen ungleichmäßig sind gleiche sie aus
    while len(groups) > 1 and len(groups[-1]) < 3:
        last_group = groups.pop()
        for item in last_group:
            index = np.argmin([len(group) for group in groups])
            groups[index].append(item)

    return groups
    
      
        
mode_select = mode()
num_of_players = num_players(mode_select)
player_names=names(num_of_players)

if mode_select==1:              
    teams=draw_teams(player_names)  #Draw Teams for Duo CashCup if Duo mode was selected
    result=create_groupstage(teams)
    
else:
    result=create_groupstage(player_names)
    print(player_names)
      
for i, group in enumerate(result):
    print(f"Gruppe {i + 1}: {group}")
