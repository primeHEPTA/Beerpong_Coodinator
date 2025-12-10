import sqlite3

class TournamentDatabase:

    def __init__(self, database_name='tournament_database.db'):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_player_stats_table()

    def create_player_stats_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                player_name TEXT,
                total_games INTEGER,
                wins INTEGER,
                defeats INTEGER,
                final_wins INTEGER,
                second_places INTEGER,
                win_ratio FLOAT
            )
        ''')
        self.conn.commit()

    def update_player_stats(self, player_data):
        for player, stats in player_data.items():
            existing_stats = self.get_player_stats(player)

            if existing_stats:
                # Wenn Spielerdaten bereits existieren, addiere die neuen Werte zu den vorhandenen
                total_games = existing_stats[1] + stats['total_games']
                wins = existing_stats[2] + stats['wins']
                defeats = existing_stats[3] + stats['defeats']
                final_wins = existing_stats[4] + stats['final_wins']
                second_places = existing_stats[5] + stats['second_places']
                win_ratio=round(wins/total_games,2)

                self.cursor.execute('''
                    UPDATE player_stats
                    SET total_games=?, wins=?, defeats=?, final_wins=?, second_places=?, win_ratio=?
                    WHERE player_name=?
                ''', (total_games, wins, defeats, final_wins, second_places, win_ratio, player))
            else:
                # Wenn Spielerdaten nicht existieren, füge einen neuen Datensatz hinzu
                win_ratio=stats['wins']/stats['total_games']
                self.cursor.execute('''
                    INSERT INTO player_stats (player_name, total_games, wins, defeats, final_wins, second_places, win_ratio)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (player, stats['total_games'], stats['wins'], stats['defeats'], stats['final_wins'], stats['second_places'], win_ratio))

        self.conn.commit()

    def get_player_stats(self, player_name):
        self.cursor.execute('''
            SELECT * FROM player_stats WHERE player_name=?
        ''', (player_name,))
        return self.cursor.fetchone()
    
    def get_stats(self):
        self.cursor.execute('''SELECT * FROM player_stats ORDER BY final_wins DESC, second_places DESC, win_ratio DESC;''' )
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()



