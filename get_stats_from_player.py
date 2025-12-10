import database_class

database = database_class.TournamentDatabase()
player_name=input("Enter playername to see stats.")
player=database.get_player_stats(player_name)
print(player)