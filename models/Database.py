import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = os.path.join("databases", "hangman_2025.db")
        self.connection = None
        self.cursor = None
        self.connect()
        self.check_database()
        self.check_words_table()

    def connect(self):
        #Ühendus andmebaasiga
        if not os.path.exists("databases"):
            os.makedirs("databases")

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def check_database(self):
        #Kontrollib, kas andmebaas ja vajalikud tabelid eksisteerivad
        if not os.path.exists(self.db_path):
            raise FileNotFoundError("Andmebaasi faili ei leitud. Rakendus lõpetab töö.")

        # Kontrollime words tabeli olemasolu
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words';")
        if not self.cursor.fetchone():
            raise ValueError("Tabel 'words' puudub. Rakendus lõpetab töö.")

        # Kontrollime leaderboard tabeli olemasolu ja loome selle vajadusel
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leaderboard';")
        if not self.cursor.fetchone():
            print("Tabel 'leaderboard' puudub, luuakse uus tabel.")
            self.cursor.execute("""
                CREATE TABLE leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    word TEXT,
                    letters TEXT,
                    game_length INTEGER,
                    game_time TEXT
                );
            """)
            self.connection.commit()

    def check_words_table(self):
        #Kontrollib, kas words tabel on tühi. Kui on, siis rakendus ei käivitu
        self.cursor.execute("SELECT COUNT(*) FROM words;")
        if self.cursor.fetchone()[0] == 0:
            raise ValueError("Tabel 'words' on tühi. Rakendus lõpetab töö.")

    def get_random_word(self, category=None):
        #Tagastab juhusliku sõna kindla kategooria järgi
        if category:
            self.cursor.execute("SELECT word FROM words WHERE category = ? ORDER BY RANDOM() LIMIT 1;", (category,))
        else:
            self.cursor.execute("SELECT word FROM words ORDER BY RANDOM() LIMIT 1;")
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_unique_categories(self):
        #Tagastab kõik unikaalsed kategooriad
        self.cursor.execute("SELECT DISTINCT category FROM words;")
        categories = [row[0] for row in self.cursor.fetchall()]
        categories.insert(0, 'Vali kategooria')  # Lisame esimeseks valiku "Vali kategooria"
        return categories

    def save_score(self, name, word, letters, game_length, game_time):
        """Salvestab mängu tulemused andmebaasi."""
        self.cursor.execute("""
            INSERT INTO leaderboard (name, word, letters, game_length, game_time)
            VALUES (?, ?, ?, ?, ?)
        """, (name, word, letters, game_length, game_time))
        self.connection.commit()

    def read_leaderboard(self):
        #Loeb ja tagastab edetabeli andmed. Kui edetabel on tühi, tagastab teavituse
        
        self.cursor.execute("SELECT name, word, letters, game_length, game_time FROM leaderboard ORDER BY game_length, LENGTH(letters);")
        data = self.cursor.fetchall()
        if not data:
            print("Edetabel on tühi. Pole ühtegi mängijat.")
        return data

    def close(self):
        """Sulgeb andmebaasi ühenduse."""
        self.connection.close()
