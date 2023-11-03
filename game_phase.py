from setup_phase import create_gameplan, create_groupstage, draw_teams, names, num_players, mode
#from tournament_class import Tournament
from get_groupname import Tournament
def get_group_name(teams, group_names):    
    for group in range(len(groups)):
        if all(team in groups[group] for team in teams):
            return group_names[group]
    return None 
   
def game_phase(tournament, group_names, playdaymatches_list):
    while True:
        command = input("Enter Command ('s' for standings, 'e' for enter scoring, '0' for termination): ")
        if command == '0':
            break
        if command == 's':
            group_name = input("Enter Groupname ('Group(number)'): ")
            if group_name in tournament.group_names:
                tournament.calculate_standings(group_name)
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
                    for i, match in enumerate(playdaymatches_list[playday - 1], 1):
                        print(f"{i}: {match[0]} vs {match[1]}")

                    choice = input("Enter the number of the match to update ('0' to exit): ")

                    if choice == '0':
                        break

                    match_number = int(choice)
                    if 1 <= match_number <= len(playdaymatches_list[playday - 1]):
                        team1, team2 = playdaymatches_list[playday - 1][match_number - 1]
                        print(f"Match: {team1} vs {team2}")
                        group_name = get_group_name([team1, team2], group_names)
                        if group_name:
                            cup_diff = int(input(f"Differenece for Match {team1} vs {team2}: "))                           
                            tournament.record_result(group_name, playday, (team1, team2), cup_diff)
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


mode_select = mode()
num_of_players = num_players(mode_select)
player_names=names(num_of_players)

if mode_select==1:              

    teams=draw_teams(player_names)  #Draw Teams for Duo CashCup if Duo mode was selected
    groups,group_names=create_groupstage(teams)
    for i, group in enumerate(groups):

        print(f"Group {i + 1}: {group}")

    gameplan,playdaymatches_list = create_gameplan(groups)
    for playday_matches in gameplan:
        print(playday_matches)
        
    tournament = Tournament(group_names,player_names, playdaymatches_list,groups)
    game_phase(tournament, group_names,playdaymatches_list)

else:
    groups,group_names=create_groupstage(player_names)
    print(group_names)
    for i, group in enumerate(groups):
        print(f"Group {i + 1}: {group}")
        
    gameplan,playdaymatches_list = create_gameplan(groups)
    #print(playdaymatches_list[0])
    for playday_matches in gameplan:
        print(playday_matches)
        
    tournament = Tournament(group_names, player_names, playdaymatches_list, groups)
    game_phase(tournament, group_names, playdaymatches_list)

    

