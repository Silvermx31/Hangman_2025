import random
from tkinter import DISABLED, NORMAL, simpledialog, messagebox

from models.Leaderboard import Leaderboard
from models.Stopwatch import Stopwatch
from models.Timer import Timer


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.stopwatch = Stopwatch(self.view.lbl_time)

        #ajasti loomine
        self.timer = Timer(
            scheduled_callback=self.view.after,
            cancel_callback=self.view.after_cancel,
            interval=5000,  #5 sek
            callback=self.change_title,
        )

#nuppude callback seaded
        self.btn_new_callback()
        self.btn_cancel_callback()
        self.btn_send_callback()
        self.btn_scoreboard_callback()
        self.view.set_timer_reset_callback(self.reset_timer)    #ajasti värk

        # Enter klahv funktsionaalsus
        self.view.bind('<Return>', lambda event: self.btn_send_click())


    def buttons_for_game(self):
        self.view.btn_new['state'] = DISABLED
        self.view.btn_send['state'] = NORMAL
        self.view.btn_cancel['state'] = NORMAL
        self.view.enrty_letter['state'] = NORMAL
        self.view.enrty_letter.focus()
        self.view.cmb_category['state'] = DISABLED

    def buttons_for_not_game(self):
        self.view.btn_new['state'] = NORMAL
        self.view.btn_send['state'] = DISABLED
        self.view.btn_cancel['state'] = DISABLED
        self.view.enrty_letter.delete(0, 'end')  # Tühjenda sisestuskast
        self.view.enrty_letter['state'] = DISABLED
        self.view.cmb_category['state'] = NORMAL

    def btn_new_callback(self):
        self.view.set_btn_new_callback(self.btn_new_click)  # meetod ilma sulgudeta

    def btn_cancel_callback(self):
        self.view.set_btn_cancel_callback(self.btn_cancel_click)

    def btn_send_callback(self):
        self.view.set_btn_send_callback(self.btn_send_click)

    def btn_scoreboard_callback(self):
        self.view.set_btn_scoreboard_callback(self.btn_scoreboard_click)

    def btn_new_click(self):
        self.buttons_for_game()
#seadistab juhusliku sõna kategooria järgi ja asendab tähed _
        self.model.start_new_game(self.view.cmb_category.current(), self.view.cmb_category.get())   # id, sõna
# Näita "sõna"kasutajale
        self.view.lbl_result.config(text=self.model.user_word)
# vigaste tähtede resettimine
        self.view.lbl_error.config(text='Vigased tähed', fg='black')
# muuda pilti
        self.view.change_image(self.model.counter)      # Või 0 sulgudesse
        self.timer.start()      # Käivita title juhuslikkus (5 sek)
        self.stopwatch.reset()  # Eelmine mäng
        self.stopwatch.start()  # Käivita aeg


    def btn_cancel_click(self):
        self.buttons_for_not_game()
        self.stopwatch.stop()
        self.timer.stop()       # Peata title juhuslikkus (5 sek)
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.title(self.model.title[0])  # esimene element title listis

    def btn_send_click(self):
        self.model.get_user_input(self.view.enrty_letter.get().strip())     # saada sisestus
        self.view.lbl_result.config(text=self.model.user_word)  # uuenda tulemust,
        self.view.lbl_error.config(text=f'Vigased tähed: {self.model.get_all_user_chars()}')
        # sisestuskast tühjendada
        self.view.enrty_letter.delete(0, 'end')     # Tühjenda sisestuskast
        if self.model.counter > 0:
            self.view.lbl_error.config(fg='red')    # muuda vigane tekst punaseks
            self.view.change_image(self.model.counter)        # muuda pilti

        self.is_game_over()

    def btn_scoreboard_click(self):
        lb = Leaderboard()
        data = lb.read_leaderboard()
        popup_window = self.view.create_popup_window()
        self.view.generate_scoreboard(popup_window, data)


        #print('Edetabel')

    def is_game_over(self):
        if self.model.counter >= 11 or '_' not in self.model.user_word:
            self.stopwatch.stop()       # peatab stopperi
            self.timer.stop()  # Peata title juhuslikkus (5 sek)
            self.buttons_for_not_game()
            player_name = simpledialog.askstring('Mäng on läbi', 'Kuidas on mängija nimi?', parent=self.view)
            messagebox.showinfo('Teade', 'Oled lisatud edetabelisse')
            #print(player_name)
            self.model.save_player_score(player_name, self.stopwatch.seconds)
            self.view.title(self.model.title[0])        # esimene element title listis

    def change_title(self):
        new_title = random.choice(self.model.titles)
        self.view.title(new_title)

    def reset_timer(self):
        self.timer.start()