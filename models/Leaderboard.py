from models.Database import Database
from models.Score import Score

class Leaderboard:
    def __init__(self):
        self.__database = Database()  # Kasutame andmebaasi ühendust

    def read_leaderboard(self):
        """Loeb ja tagastab edetabeli andmed SQLite andmebaasist."""
        data = self.__database.read_leaderboard()
        return [Score(*row) for row in data]  # Tagastame tulemused Score objektidena

    def save_score(self, name, word, letters, game_length, game_time):
        """Salvestab mängu tulemused edetabelisse."""
        self.__database.save_score(name, word, letters, game_length, game_time)
