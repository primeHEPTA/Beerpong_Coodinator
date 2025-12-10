from setup_phase import create_gameplan, create_groupstage, draw_teams, names, num_players, mode, save_tournament_data, load_tournament_data, generate_filename
#from tournament_class import Tournament
from tournament_class_test import Tournament
import database_class
def get_group_name(teams):
    
    groups=tournament.groups
    for group in groups:
        if all(team in groups[group] for team in teams):
            group_name=group
            return group_name
    return None

def is_group_phase_completed(tournament):
    
    total_expected_matches = sum(len(matches) for matches in tournament.playdaymatches_list)
    total_played_matches = sum(len(matches) for group_results in tournament.results.values() for matches in group_results.values())

    return total_played_matches == total_expected_matches

def write_standings_to_file(tournament):
    base_filename = tournament.filename.rsplit('.', 1)[0]  # Entferne die letzte Dateiendung
    standings_filename = f"{base_filename}_groupphase_results.txt"

    with open(standings_filename, "w") as file:
        for group_name in tournament.group_names:
            file.write(f"Standings for '{group_name}':\n")
            file.write("team/player\tgames\twins\tdefeats\tdifference\tpoints\n")

            standings = tournament.standings.get(group_name, [])
            for team, stats in standings:
                if team in tournament.groups[group_name]:
                    file.write(f"{team}\t\t{stats[0]}\t{stats[1]}\t{stats[2]}\t{stats[3]}\t\t{stats[4]}\n")
            
            file.write("\n")
            
def group_phase(tournament, playdaymatches_list):
    while True:
        if is_group_phase_completed(tournament):
           print("Group stage is completed!")
           break
        command = input("Enter Command ('s' for standings, 'e' for enter scoring, '0' for termination): ")
        if command == '0':
            break
        if command == 's':

            if len(tournament.group_names)==1:
                #tournament.calculate_standings(tournament.group_names[0])
                tournament.display_standings(tournament.group_names[0])
            else:
                group_name = input("Enter Groupname ('Group(number)'): ")
                if group_name in tournament.group_names:
                    #tournament.calculate_standings(group_name)
                    tournament.display_standings(group_name)
                else:
                    print(f"Group '{group_name}' does not exist! Please note case sensitivity!")
        elif command == 'e':
            playday = input("Which Matchday ('0' for termination): ")
            if playday == '0':
                break

            try:
                playday = int(playday)
            except ValueError:
                print("Invalid Matchday! Please enter a valid number")
                continue

            if playday <= 0 or playday > len(playdaymatches_list):
                print(f"There is no Matchday {playday}.")
                continue

            while True:
                try:
                    if is_group_phase_completed(tournament):
                        exit
                    for i, match in enumerate(playdaymatches_list[playday - 1], 1):
                        print(f"{i}: {match[0]} vs {match[1]}")

                    choice = input("number of the match to update ('0' to exit): ")

                    if choice == '0':
                        break

                    match_number = int(choice)
                    if 1 <= match_number <= len(playdaymatches_list[playday - 1]):
                        team1, team2 = playdaymatches_list[playday - 1][match_number - 1]
                        print(f"Match: {team1} vs {team2}")
                        group_name = get_group_name([team1, team2])
                        if group_name:
                            cup_diff = int(input(f"Differenece for Match {team1} vs {team2}: "))                           
                            tournament.record_result(group_name, playday, (team1, team2), cup_diff)
                            for group_name in tournament.group_names:
                                tournament.calculate_standings(group_name)
                            save_tournament_data(tournament,load_filename)

                        else:
                            print("Group not found for the selected teams.")
                    else:
                        print("Invalid match number. Choose a valid match or '0' to exit.")

                except ValueError:
                    print("Invalid Input! Cup difference should be a number.")
        else:
            print("Invalid command! Use 's' for standings, 'e' for enter scoring, '0' for termination ")



####################################
#MAIN
####################################

load_filename=generate_filename()
knockout_results_filename = load_filename.rsplit('.', 1)[0] + "_knockout_results.txt"
while True:
    load=input("Do you want to load an already existing tournament (Yes/No): ").strip().lower()
    if load=='yes':
        tournament,load_filename=load_tournament_data()
        if tournament:
            print("Tournament data loaded.")
        break
    if load=='no':
        mode_select = mode()
        num_of_players = num_players(mode_select)
        player_names=names(num_of_players)
        x={}
        if mode_select==1:              

            player_names,teams=draw_teams(player_names)  #Draw Teams for Duo CashCup if Duo mode was selected
            x=teams

        groups,group_names=create_groupstage(player_names)
        for i, group in enumerate(groups):
            print(f"Group {i + 1}: {group}")
                
        gameplan,playdaymatches_list = create_gameplan(groups)
        for playday_matches in gameplan:
            print(playday_matches)
        
        tournament = Tournament(group_names, player_names, playdaymatches_list, groups,load_filename,x)
        save_tournament_data(tournament,load_filename)
        break
    else:
        print("Invalid Input! Enter (Yes/No).")
      
group_phase(tournament, tournament.playdaymatches_list)
if is_group_phase_completed(tournament):
    write_standings_to_file(tournament)
    if tournament.is_tournament_finished==False:
        if len(tournament.group_names)==1:
            tournament.create_final()
            tournament.display_knockout_results(knockout_results_filename)
            save_tournament_data(tournament,load_filename)
        else:
            top_teams=tournament.get_top_two_teams_per_group()
            resulting_matchups = tournament.create_knockout_stage(top_teams)
            ko_stage=tournament.get_knockout_round(resulting_matchups)          
            print(resulting_matchups)
            next_round_matchups=tournament.play_knockout_round(ko_stage, resulting_matchups)
            while ko_stage!='Final':           
                print(next_round_matchups)
                ko_stage=tournament.get_knockout_round(next_round_matchups)
                next_round_matchups=tournament.play_knockout_round(ko_stage, next_round_matchups)            
                save_tournament_data(tournament,load_filename)
            if ko_stage=='Final':
                tournament.display_knockout_results(knockout_results_filename)
                save_tournament_data(tournament,load_filename)
        player_data=tournament.player_data
        database = database_class.TournamentDatabase()
        database.update_player_stats(player_data)
        database.close_connection()
    else:
        print("Tournament is already finished.")
            