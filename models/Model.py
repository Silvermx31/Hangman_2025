import glob
import os
import random
from datetime import datetime

from models.FileObject import FileObject
from models.Leaderboard import Leaderboard


class Model:

    def __init__(self):
        self.__image_files = [] # tühi list piltide jaoks
        self.load_images('images')
        self.__file_object = FileObject('databases', 'words.txt')
        self.__categories = self.__file_object.get_unique_categories()      # unikaalsed kategooriad
        #print(self.__file_object.get_random_word('Lammas'))
        self.__scoreboard = Leaderboard()       # Loo edetabeli objekt (teeb vajadusel faili)

        self.titles = ['Poomismäng 2025', 'Kas jäd magama?', 'Ma ootan su käiku', 'Sisesta juba see täht!', 'Zzzz..']

# mängu muutujad

        self.__new_word = None  # Sõna mida ära arvata
        self.__user_word = []   # kõik kasutaja leitud tähed
        self.__counter = 0      # vigade loendur
        self.__all_user_chars = []  # kõik valesti sisestatud tähed



    def load_images(self, folder):
        if not os.path.exists(folder):
            raise FileNotFoundError(f'Kausta {folder} ei leitud. ')

        images = glob.glob(os.path.join(folder, '*.png'))       # kaustast võetakse kõik png failid
        if not images:
            raise FileNotFoundError(f'Kaustas {folder} ei ole pilte(.PNG). ')

        self.__image_files = images

    def start_new_game(self, category_id, category):
        if category_id == 0:
            category = None

        self.__new_word = self.__file_object.get_random_word(category)      # juhuslik sõna
        self.__user_word = []       # Algseis
        self.__counter = 0      # Algseis
        self.__all_user_chars = []  #Algseis

        # Asenda sõnas kõik tähed allkriipsuga  m a j a => _ _ _ _
        for x in range(len(self.__new_word)):
            self.__user_word.append('_')

    def get_user_input(self, user_input):
        #user input on sisestuskasti kirjutatud
        if user_input:
            entry_letter = user_input[:1]       # Esimene märk sisestusest
            if entry_letter.lower() in self.__new_word.lower():
                self.change_user_input(entry_letter)        #leiti täht
            else:       # Ei leitud tähte
                self.__counter += 1
                self.__all_user_chars.append(entry_letter.upper())

    def change_user_input(self, entry_letter):
        # Asenda kõik _ leitud tähtedega
        current_word = self.char_to_list(self.__new_word)       # current word on listi põhjal äratuntav sõna
        x = 0
        for c in current_word:
            if c.lower() == entry_letter.lower():
                self.__user_word[x] = entry_letter.upper()
            x += 1

    @staticmethod
    def char_to_list(word):
        # String to List, test => ['t', 'e', 's', 't']
        chars = []
        chars[:0] = word
        return chars

    def get_all_user_chars(self):
        return ', '.join(self.__all_user_chars)             # List tehakse komaga eraldatud stringiks

    def save_player_score(self, name, seconds):
        today = datetime.now().strftime('%Y-%m-%d %T')          # Hetke kuupäev ja kell: 2025-02-05 14:12:29

        if not name.strip():    # Kui nime ei ole
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])

        with open(self.__scoreboard.file_path, 'a', encoding='utf-8') as f:
            line = ';'.join([name.strip(), self.__new_word, self.get_all_user_chars(), str(seconds), today])
            f.write(line + '\n')


    # Getters
    @property
    def image_files(self):
        "Tagastab piltide listi"
        return self.__image_files

    @property
    def categories(self):
        return self.__categories        #tagastab kategooriate listi

    @property
    def user_word(self):
        return self.__user_word     #Tagastab kasutaja leitud tähed

    @property
    def counter(self):
        return self.__counter   # tagastab vigade arvu
