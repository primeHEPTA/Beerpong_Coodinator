import database_class

database = database_class.TournamentDatabase()
stats=database.get_stats()
print(stats)