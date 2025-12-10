import database_class

database = database_class.TournamentDatabase()
database.create_player_stats_table()
database.conn.commit()
database.close_connection()
