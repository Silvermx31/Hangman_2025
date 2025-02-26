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

        # Ajasti loomine
        self.timer = Timer(
            scheduled_callback=self.view.after,
            cancel_callback=self.view.after_cancel,
            interval=5000,  # 5 sek
            callback=self.change_title,
        )

        # Nuppude callback seaded
        self.btn_new_callback()
        self.btn_cancel_callback()
        self.btn_send_callback()
        self.btn_scoreboard_callback()
        self.view.set_timer_reset_callback(self.reset_timer)  # Ajasti värk

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
        self.view.set_btn_new_callback(self.btn_new_click)  # Meetod ilma sulgudeta

    def btn_cancel_callback(self):
        self.view.set_btn_cancel_callback(self.btn_cancel_click)

    def btn_send_callback(self):
        self.view.set_btn_send_callback(self.btn_send_click)

    def btn_scoreboard_callback(self):
        self.view.set_btn_scoreboard_callback(self.btn_scoreboard_click)

    def btn_new_click(self):
        self.buttons_for_game()
        self.model.start_new_game(self.view.cmb_category.current(), self.view.cmb_category.get())
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.lbl_error.config(text='Vigased tähed', fg='black')
        self.view.change_image(self.model.counter)
        self.timer.start()
        self.stopwatch.reset()
        self.stopwatch.start()

    def btn_cancel_click(self):
        self.buttons_for_not_game()
        self.stopwatch.stop()
        self.timer.stop()
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.title(self.model.titles[0])

    def btn_send_click(self):
        self.model.get_user_input(self.view.enrty_letter.get().strip())
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.lbl_error.config(text=f'Vigased tähed: {self.model.get_all_user_chars()}')
        self.view.enrty_letter.delete(0, 'end')
        if self.model.counter > 0:
            self.view.lbl_error.config(fg='red')
            self.view.change_image(self.model.counter)
        self.is_game_over()

    def btn_scoreboard_click(self):
        data = self.model.read_leaderboard()
        if not data:
            messagebox.showinfo("Edetabel", "Edetabelis pole ühtegi kirjet.")
        else:
            popup_window = self.view.create_popup_window()
            self.view.generate_scoreboard(popup_window, data)

    def is_game_over(self):
        if self.model.counter >= 11 or '_' not in self.model.user_word:
            self.stopwatch.stop()
            self.timer.stop()
            self.buttons_for_not_game()
            player_name = simpledialog.askstring('Mäng on läbi', 'Kuidas on mängija nimi?', parent=self.view)
            if player_name:
                self.model.save_player_score(player_name, self.stopwatch.seconds)
                messagebox.showinfo('Teade', 'Oled lisatud edetabelisse')
            self.view.title(self.model.titles[0])

    def change_title(self):
        new_title = random.choice(self.model.titles)
        self.view.title(new_title)

    def reset_timer(self):
        self.timer.start()
