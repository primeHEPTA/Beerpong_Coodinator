
class Tournament:

    def __init__(self, group_names, player_names, playdaymatches_list,groups,filename,teams):
        self.group_names = group_names
        self.player_names = player_names
        self.playdaymatches_list = playdaymatches_list
        self.filename=filename
        self.team_dic=teams
        self.player_stats = {player: {'final_wins': 0, 'second_places': 0} for player in player_names}
        self.knockout_results = {'Round of 64': [], 'Round of 32': [], 'Round of 16': [],'Round of 8': [], 'Quarterfinals': [], 'Semifinals': [], 'Final': []}
        self.groups = {group_name: group for group_name, group in zip(group_names, groups)}
        self.results = {group: {} for group in group_names}
        self.standings = {group: {} for group in group_names}
        self.group_phase_data_updated=False
        self.is_tournament_finished=False
        self.player_data={}

    def record_result(self, group, playday, match, cup_diff):
        if group not in self.results:
            print(f"Gruppe '{group}' existiert nicht.")
            return

        if playday not in self.results[group]:
            self.results[group][playday] = []

        existing_result = None

    # Überprüfen, ob das Ergebnis bereits existiert
        for i, (existing_match, _) in enumerate(self.results[group][playday]):
            if existing_match == match:
                existing_result = i
                break   

        if existing_result is not None:
        # Das Ergebnis existiert bereits, Benutzer um Bestätigung bitten
            confirmation = input("An entry for this match already exists. Do you want to overwrite it? (Yes/No): ").strip().lower()
            if  confirmation == 'yes' or confirmation=='Yes':
            # Lösche das vorhandene Ergebnis, da es überschrieben wird
                del self.results[group][playday][existing_result]
            if confirmation=='no' or confirmation=='No':
                return

    # Füge das neue Ergebnis hinzu
        self.results[group][playday].append((match, cup_diff))

    def calculate_standings(self, group):
        if group not in self.groups:
            print(f"Group '{group}' does not exist.")
            return

    # Tabellenstände berechnen
        standings = {team: [0, 0, 0, 0, 0] for team in self.player_names if team in self.groups[group]}
    # [Spiele, Siege, Niederlagen, Becherdifferenz, Punkte]

        for playday, results in self.results[group].items():
            for match, cup_diff in results:
                team1, team2 = match

                if cup_diff > 0:
                    standings[team1][1] += 1  # Sieg für Team 1
                    standings[team2][2] += 1  # Niederlage für Team 2
                    standings[team1][4] += 3  # Punkte für Team 1
                elif cup_diff < 0:
                    standings[team1][2] += 1  # Niederlage für Team 1
                    standings[team2][1] += 1  # Sieg für Team 2
                    standings[team2][4] += 3  # Punkte für Team 2

            # Becherdifferenz hinzufügen
                standings[team1][3] += cup_diff
                standings[team2][3] -= cup_diff

            # Gespielte Spiele erhöhen
                standings[team1][0] += 1
                standings[team2][0] += 1

    # Nach Punkten sortieren
        sorted_standings = sorted(standings.items(), key=lambda x: (x[1][4], x[1][3]), reverse=True)
        self.standings[group] = sorted_standings

    def display_standings(self, group):
        if group not in self.groups:
            print(f"Group '{group}' does not exist.")
            return

        if group not in self.standings:
            print(f"Standings for Group '{group}' are not calculated yet.")
            return

        print(f"Standings for '{group}':")
        print("team/player\tgames\twins\tdefeats\tdifference\tpoints")
        standings = self.standings[group]

        for team, stats in standings:
            if team in self.groups[group]: #gebe nur teams/spieler der jeweiligen Gruppe aus
                print(f"{team}\t\t{stats[0]}\t{stats[1]}\t{stats[2]}\t{stats[3]}\t\t{stats[4]}")
    
    def create_final(self):
        num_groups=len(self.group_names)
        if num_groups==1:
            while True:
                try:
                    round_name='Final'
                    print(round_name)
                    group=self.group_names[0]
                    group_standings=self.standings[group]
                    first_team = group_standings[0][0]
                    second_team = group_standings[1][0]
                    cup_diff = int(input(f"Difference for Match {first_team} vs {second_team}: "))
                    self.record_knockout_result(round_name, (first_team,second_team),cup_diff,True)
                    data=self.adjust_player_data()
                    self.player_data=data
                    winner = first_team if cup_diff > 0 else second_team
                    print(f"Congratulations! Winner of the tournament is:{winner}.")
                    self.is_tournament_finished=True
                    return
                except ValueError:
                    print("Invalid input! Please enter a valid integer.")

    def adjust_player_data(self):
        player_data_new={}
        if len(self.team_dic)!=0:
            for team, players in self.team_dic.items():
                    for player in players:
                        player_data_new[player] = {
                            'total_games': self.player_data[team]['total_games'],
                            'wins': self.player_data[team]['wins'],
                            'defeats': self.player_data[team]['defeats'],
                            'final_wins': self.player_data[team]['final_wins'],
                            'second_places': self.player_data[team]['second_places']
                        }
            return player_data_new
        else:
            return self.player_data

    def get_top_two_teams_per_group(self):
        top_two_teams = []

        for group_name in self.group_names:
            if group_name in self.standings:
                group_standings = self.standings[group_name]

                    # Überprüfen, ob es genügend Teams in der Gruppe gibt
                if len(group_standings) >= 2:
                    top_team = group_standings[0][0]
                    second_team = group_standings[1][0]
                    top_teams=top_team,second_team
                    top_two_teams.extend(top_teams)
            
        return top_two_teams
    
    def create_knockout_stage(self,top_teams):
        # Erweitere die Liste auf eine Zweierpotenz

        next_power_of_two = 2 ** ((len(top_teams) - 1).bit_length())
        num_missing_teams=next_power_of_two-len(top_teams)
        for i in range(num_missing_teams):
            top_teams.append("None")
        pairings = []
        for i in range(0, next_power_of_two, 4):
            team1 = top_teams[i]
            team2 = top_teams[i + 2]
            pairing = (team1, team2)
            pairings.append(pairing)

        for i in range(1, next_power_of_two, 4):
            team1 = top_teams[i]
            team2 = top_teams[i + 2]
            pairing = (team1, team2)
            pairings.append(pairing)
        return pairings

    def get_knockout_round(self,matchups):
        num_matches=len(matchups)*2
        rounds = {
            2: "Final",
            4: "Semifinals",
            8: "Quarterfinals",
            16: "Round of 16",
            32: "Round of 32",
            64: "Round of 64",
            # Füge weitere Runden hinzu, wenn nötig
        }

        for matches, round_name in rounds.items():
            if num_matches == matches:
                return round_name

        
        if num_matches > 64:
            return "Round of 128"

        return "Unknown Round"
    
    def play_knockout_round(self, round_name, matchups):
        print(f"\n{round_name}:")
        next_round_teams = []
        for i, match in enumerate(matchups):
            team1, team2 = match
            if 'None' in team1 or 'None' in team2:
                winner = team1 if 'None' in team2 else team2
                next_round_teams.insert(i, winner)

        while True:
            try:

                if len(matchups)!=len(next_round_teams):
                    for i, match in enumerate(matchups, 1):
                        print(f"{i}: {match[0]} vs {match[1]}")
                    choice = input(f"Enter the number of the match to update: ")

                    match_number = int(choice)
                    if 1 <= match_number <= len(matchups):
                        team1, team2 = matchups[match_number - 1]
                        if 'None' in team1 or 'None' in team2:
                            winner = team1 if 'None' in team2 else team2
                            print(f"Match {team1} vs {team2} is a bye. {winner} advances to the next round.")
                            
                        else:
                            cup_diff = int(input(f"Difference for Match {team1} vs {team2}: "))
                            winner = team1 if cup_diff > 0 else team2
                            next_round_teams.insert(match_number-1,winner)
                            if round_name!='Final':
                                self.record_knockout_result(round_name, (team1, team2), cup_diff,False)
                            else:
                                self.record_knockout_result(round_name, (team1, team2), cup_diff, True)
                                data=self.adjust_player_data()
                                self.player_data=data
                                winner = team1 if cup_diff > 0 else team2
                                print(f"Congratulations! Winner of the tournament is:{winner}.")
                                self.is_tournament_finished=True
                                return
                    else:
                            print("Invalid match number. Choose a valid match.")
                else:
                    
                    break
            except ValueError:
                print("Invalid input! Please enter a valid integer.")

        if round_name != 'Final':
            next_round_matchups = [(next_round_teams[i], next_round_teams[i + 1]) for i in range(0, len(next_round_teams), 2)]
            return next_round_matchups

    def record_knockout_result(self, round_name, match, cup_diff,is_final):
        if round_name not in self.knockout_results:
            print(f"Unrecognized K.O. round: {round_name}")
            return
        
        match_data=(match,cup_diff)
        if match_data not in self.knockout_results[round_name]:
            self.knockout_results[round_name].append(match_data)
            
            team1, team2 = match
            winner, loser = (team1, team2) if cup_diff > 0 else (team2, team1)
            self.gather_player_data(winner, loser, cup_diff, is_final)
    
    def display_knockout_results(self,filename):
        with open(filename, "w") as file:
            for round_name, results in self.knockout_results.items():
                file.write(f"{round_name} Results:\n")
                for i, (match, cup_diff) in enumerate(results, 1):
                    file.write(f"{i}: {match[0]} vs {match[1]}, Difference: {cup_diff}\n")

    def gather_player_data(self, winner, loser, cup_diff, is_final):
        if not self.group_phase_data_updated:
            for group_name, standings in self.standings.items():
                for player, stats in standings:
                    if player not in self.player_data:
                        self.player_data[player] = {
                            'total_games': 0,
                            'wins': 0,
                            'defeats': 0,
                            'final_wins': 0,
                            'second_places': 0
                        }

                    total_games = int(self.player_data[player]['total_games'])
                    wins = stats[1]
                    defeats = stats[2]

                    self.player_data[player] = {
                        'total_games': total_games + stats[0],
                        'wins': wins,
                        'defeats': defeats,
                        'final_wins': 0,
                        'second_places': 0
                    }

            self.group_phase_data_updated = True
        # Restlicher Code bleibt unverändert
        total_games_winner, wins_winner, defeats_winner = int(self.player_data[winner]['total_games']), int(
            self.player_data[winner]['wins']), int(self.player_data[winner]['defeats'])
        total_games_winner += 1
        wins_winner += 1
        self.player_data[winner] = {
            'total_games': total_games_winner,
            'wins': wins_winner,
            'defeats': defeats_winner,
            'final_wins': 1 if is_final else 0,
            'second_places': 0
        }

        total_games_loser, wins_loser, defeats_loser = int(self.player_data[loser]['total_games']), int(
            self.player_data[loser]['wins']), int(self.player_data[loser]['defeats'])
        total_games_loser += 1
        defeats_loser += 1
        self.player_data[loser] = {
            'total_games': total_games_loser,
            'wins': wins_loser,
            'defeats': defeats_loser,
            'final_wins': 0,
            'second_places': 1 if is_final else 0
        }
        #print(self.player_data)
        return self.player_data
