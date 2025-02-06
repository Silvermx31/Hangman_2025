import os
import random


class FileObject:

    def __init__(self, folder, filename):
        path = os.path.join(folder, filename)   # filename/words.txt
        self.__data = self._read_file(path)


    @staticmethod
    def _read_file(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f'Faili {path} ei leitud. ')        #faili sisu

        data = {}   # Dictionary. Muutja:Väärtus   sõna:kategooria
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            if not lines:
                raise ValueError(f'Fail {path} on tühi. ')

            # Esimene rida on päis
            header = lines[0].strip().split(';')  #['word','category']
            if len(header) != 2:
                raise ValueError('Faili formaat on vale')

            # Loe ülejäänud read
            for line in lines[1:]:
                word, category = line.strip().split(';')
                if category not in data:
                    data[category] = []     # lisa kategooria tühi dictionary{}
                data[category].append(word)     # Lisa sõna kategooriasse

        return data     # Tagasta faili sisu:   {'hoone': ['suvila'], 'loom': ['lammas'], 'amet': ['vetelpäästja']}

    def get_unique_categories(self):
        categories = list(self.__data.keys())   # Võtmetest tehakse list
        categories.sort()
        #lisa "vali kategooria" listi esimeseks elemendiks
        categories.insert(0, 'Vali kategooria')
        return [category.capitalize() for category in categories]   # tagastab kategooriate nimede listi, esimene täht Suur

    def get_random_word(self, category):
        if category is None:    #Kategooriat ei ole st kõik sõnad lubatud
            all_words = [word for words in self.__data.values() for word in words]
            return random.choice(all_words) if all_words else None

        category = category.lower()
        if category in self.__data:
            return random.choice(self.__data[category]) if self.__data[category] else None
        # kui kategooriat ei leitud
        return None