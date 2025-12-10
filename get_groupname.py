class Tournament:

    def __init__(self, group_names, player_names, playdaymatches_list,groups):
        self.group_names = group_names
        self.player_names = player_names
        self.playdaymatches_list = playdaymatches_list
        self.groups = {group_name: group for group_name, group in zip(group_names, groups)}
        self.results = {group: {} for group in group_names}
        self.standings = {group: {} for group in group_names}

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
        standings = {team: [0, 0, 0, 0, 0] for team in self.player_names}
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
            print(f"Standings for Group '{group}' are not yet calculated.")
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
            group=self.group_names[0]
            group_standings=self.standings[group]
            if len(group_standings)>=4:
                first_team = group_standings[0][0]
                second_team = group_standings[1][0]
                third_team = group_standings[2][0]
                fourth_team = group_standings[3][0]
                game_for_third_place=(third_team,fourth_team)
                final=(first_team,second_team)
                print(f"Game for third place:{game_for_third_place}")
                print(f"Final:{final}")
                matches=(game_for_third_place,final)
                return matches
            else:
                first_team = group_standings[0][0]
                second_team = group_standings[1][0]
                final=(first_team,second_team)
                print(f"Final:{final}")
                return final

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
            top_teams.append(f"None{i}")
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
        for match in matchups:
            team1, team2 = match
            print()
            # Überprüfe Spiele mit 'None' (Freilos für ein Team)
            if 'None' in team1 or 'None' in team2:
                winner = team1 if team2 == 'None' else team2
                next_round_teams.insert(match,winner)
                print(f"Match {team1} vs {team2} is a bye. {winner} advances to the next round.")
            else:
                while True:
                    try:
                        for i, match in enumerate(matchups, 1):
                            print(f"{i}: {match[0]} vs {match[1]}")
                        choice = input("Enter the number of the match to update (0 to skip): ")

                        if choice == '0':
                            break

                        match_number = int(choice)
                        if 1 <= match_number <= len(matchups):
                            team1, team2 = matchups[match_number - 1]
                            cup_diff = int(input(f"Difference for Match {team1} vs {team2}: "))
                            winner = team1 if cup_diff > 0 else team2
                            break
                        else:
                            print("Invalid match number. Choose a valid match.")
                    except ValueError:
                        print("Invalid input! Please enter a valid integer.")
                    
                next_round_teams.insert(match_number-1,winner)

        if round_name != 'Final':
            next_round_matchups = [(next_round_teams[i], next_round_teams[i + 1]) for i in range(0, len(next_round_teams), 2)]
            return next_round_matchups
        else:
            return
