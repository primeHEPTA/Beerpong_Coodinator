import random

import numpy as np

from setup_phase import create_gameplan, create_groupstage, draw_teams, names, num_players,mode



class Tournament:

    def __init__(self, group_names):

        self.group_names = group_names

        self.groups = {group: [] for group in group_names}

        self.results = {group: {} for group in group_names}

        self.standings = {group: {} for group in group_names}



    

    def record_result(self, group, playday, match, becher_diff):

        if group not in self.results:

            print(f"Gruppe '{group}' existiert nicht.")

            return

        

        if playday not in self.results[group]:

            self.results[group][playday] = []

        

        self.results[group][playday].append((match, becher_diff))



    def calculate_standings(self, group):

        if group not in self.groups:

            print(f"Gruppe '{group}' existiert nicht.")

            return

        

        # Tabellenstände berechnen

        standings = {team: [0, 0, 0, 0, 0] for team in self.groups[group]}

        # [Spiele, Siege, Niederlagen, Becherdifferenz, Punkte]

        

        for playday, results in self.results[group].items():

            for match, becher_diff in results:

                team1, team2 = match

                if becher_diff > 0:

                    standings[team1][1] += 1  # Sieg für Team 1

                    standings[team2][2] += 1  # Niederlage für Team 2

                    standings[team1][4] += 3  # Punkte für Team 1

                elif becher_diff < 0:

                    standings[team1][2] += 1  # Niederlage für Team 1

                    standings[team2][1] += 1  # Sieg für Team 2

                    standings[team2][4] += 3  # Punkte für Team 2

                # Becherdifferenz hinzufügen

                standings[team1][3] += becher_diff

                standings[team2][3] -= becher_diff

                # Gespielte Spiele erhöhen

                standings[team1][0] += 1

                standings[team2][0] += 1

        

        # Nach Punkten sortieren

        sorted_standings = sorted(standings.items(), key=lambda x: (x[1][4], x[1][3]), reverse=True)

        self.standings[group] = sorted_standings



    def display_standings(self, group):

        if group not in self.groups:

            print(f"Gruppe '{group}' existiert nicht.")

            return

        

        if group not in self.standings:

            print(f"Tabellenstände für Gruppe '{group}' sind noch nicht berechnet.")

            return

        

        print(f"Tabellenstände für Gruppe '{group}':")

        print("Team\tSpiele\tSiege\tNiederlagen\tBecherdiff\tPunkte")

        for team, stats in self.standings[group]:

            print(f"{team}\t{stats[0]}\t{stats[1]}\t{stats[2]}\t{stats[3]}\t{stats[4]}")

   



def game_phase(tournament, gameplan):

    while True:

        playday = input("Welcher Spieltag ('0' zum Beenden): ")

        if playday == '0':

            break



        found_playday = False

        for playday_matches in gameplan:

            if playday_matches.startswith(f"Spieltag {playday}"):

                found_playday = True

                matches = playday_matches[len(f"Spieltag {playday}: "):]

                matches = matches.split(", ")

                for match in matches:

                    teams = match.split(" vs ")

                    if len(teams) == 2:

                        team1, team2 = teams

                        becher_diff = int(input(f"Becherdifferenz im Spiel {team1} vs {team2}: "))

                        tournament.record_result("Group1", int(playday), (team1, team2), becher_diff)

                    else:

                        print(f"Ungültiges Spielformat: {match}")



        if not found_playday:

            print(f"Es gibt keine Spiele für Spieltag {playday}.")



        for group_name in group_names:

            tournament.calculate_standings(group_name)

            tournament.display_standings(group_name)       



#MAIN





mode_select = mode()

num_of_players = num_players(mode_select)

player_names=names(num_of_players)



if mode_select==1:              

    teams=draw_teams(player_names)  #Draw Teams for Duo CashCup if Duo mode was selected

    groups,group_names=create_groupstage(teams)

    for i, group in enumerate(groups):

        print(f"Group {i + 1}: {group}")

    gameplan = create_gameplan(groups)

    for playday_matches in gameplan:

        print(playday_matches)

    tournament = Tournament(group_names)

    game_phase(tournament,gameplan)

else:

    groups,group_names=create_groupstage(player_names)

  

    for i, group in enumerate(groups):

        print(f"Group {i + 1}: {group}")

    gameplan = create_gameplan(groups)

    for playday_matches in gameplan:

        print(playday_matches)

    tournament = Tournament(group_names)

    game_phase(tournament,gameplan)

    

