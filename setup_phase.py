import random
import numpy as np
import datetime
import pickle

def num_players(m):
    while True:
        try:
            if m == 0:  # SOLO CashCup selected
                x = int(input("Enter number of players: "))
                if x <= 0:
                    print("You must enter a positive number of players.")
                elif x >= 3:
                    print(f"You have entered {x} players.")
                    return x
                else:
                    print("You need at least three players.")
            if m == 1:  # DUO CashCup selected
                x = int(input("Enter an even number of players greater or equal than six: "))
                if x <= 0:
                    print("You must enter a positive number of players.")
                elif x >= 6:
                    if x % 2 != 0:
                        print("You must enter an even number of players")
                    else:
                        print(f"You have entered {x} players.")
                        return x
                else:
                    print("You need at least six players.")
        except ValueError:
            print("Invalid input! Please enter a valid number of players.")

def names(x):
    player_names = []
    
    for i in range(x):
        while True:
            name = input(f"Enter the name of player {i + 1}: ")
            if name in player_names:
                print("Name already exists. Please choose a different name.")
            if 'none' in name.strip().lower() or name=='':
                print("Invalid name!Choose a different name")
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
            
def draw_teams(player_names):
    
    if len(player_names) % 2 != 0 or len(player_names) < 4:
        print("The number of players is not ideal! Could not create proper teams.")
    
    teams = []
    team_names = []
    team_dic={}
    
    
    for i in range(len(player_names) // 2):
        team = [player_names[i * 2], player_names[i * 2 + 1]]
        teams.append(team)

        # Ausgabe der Teams mit Spielernamen
    print("****************TEAMS****************")
    for i, team in enumerate(teams):
        print(f"Team {i + 1}: {', '.join(team)}")

    for i, team in enumerate(teams):
        while True:
            team_name = input(f"Enter the name for Team {i + 1}: ")
            if team_name not in team_names:
                team_names.append(team_name)
                break
            else:
                print("Team name already exists. Please choose a different name.")
    team_dic=dict(zip(team_names,teams))
    print(team_dic)
    return team_names,team_dic

def create_groupstage(arr):
    n = len(arr)
    if n <= 5:
        # Wenn die Liste klein genug ist, gib einzelne Gruppe zurück
        group_names=["Group1"]
        return [arr], group_names
    
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
    group_names = [f"Group{i + 1}" for i in range(len(groups))]       
    return groups, group_names 

def create_gameplan(groups):
    num_groups = len(groups)
    num_teams_per_group = max(len(group) for group in groups)
    num_playdays = num_teams_per_group - 1 if num_teams_per_group % 2 == 0 else num_teams_per_group
    
    playdaymatches_list=[]
    gameplan = []
    played_matches = set()  # Verfolgen der bereits gespielten Spiele

    for playday in range(1, num_playdays + 1):
        playday_matches = []
        played_teams = set()

        for group in groups:
            for i, team in enumerate(group):
                if team not in played_teams:
                    available_opponents = [x for x in group if x != team and x not in played_teams]
                    if available_opponents:
                        opponent = available_opponents[0]
                        match = (team, opponent)

                        # Überprüfen, ob dieses Spiel bereits gespielt wurde
                        if (team, opponent) not in played_matches and (opponent, team) not in played_matches:
                            playday_matches.append(match)
                            played_teams.add(team)
                            played_teams.add(opponent)
                            played_matches.add(match)
        
        if playday_matches:
            gameplan.append(f"Spieltag {playday}: {playday_matches}")
            playdaymatches_list.append(playday_matches)
        # Teams aussetzen
        for group in groups:
            if len(group) % 2 == 0:
                group.append(group.pop(1))  # Verschiebe das zweite Team an das Ende
            else:
                group.insert(1, group.pop(-1))  # Verschiebe das letzte Team an die zweite Position

        if playday == num_playdays - 1:
            # Teams, die ausgesetzt haben, spielen am letzten Spieltag untereinander
            final_playday_matches = []
            for group in groups:
                for i, team in enumerate(group):
                    for j in range(i + 1, len(group)):
                        opponent = group[j]
                        match = (team, opponent)
                        if match not in played_matches and (opponent, team) not in played_matches:
                            final_playday_matches.append(match)
            if final_playday_matches:
                gameplan.append(f"Spieltag {num_playdays}: {final_playday_matches}")
                playdaymatches_list.append(final_playday_matches)
            # Kein weiterer Spieltag erforderlich
            break

    return gameplan, playdaymatches_list

def save_tournament_data(tournament,filename):
    
    with open(filename, "wb") as file:
        pickle.dump(tournament, file)
    return filename

def load_tournament_data():
    while True:
        filename = input("Enter the name of the file to load: ").strip()

        try:
            with open(filename, "rb") as file:
                tournament = pickle.load(file)
            return tournament,filename
        except FileNotFoundError:
            print(f" '{filename}' not found. Please enter a valid file name.")
        except pickle.PickleError as pe:
            print(f"Error while loading/pickling data: {str(pe)}")

def generate_filename(extension="dat"):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"_tournaments/Tournament_{current_datetime}.{extension}"
    return filename