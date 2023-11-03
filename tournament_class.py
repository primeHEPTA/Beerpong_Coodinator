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



    

