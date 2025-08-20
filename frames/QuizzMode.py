from functools import partial
from random import shuffle

import customtkinter as ctk
from globals import OPER_FOLDER
from helper_fn import mix, get_text_from_file

"""Shows us a frame with a question and 4 options of answer.
   There is 1 `correct button` and 3 `incorrect` ones, every question 
   their position is mixed. User ca only go to the next question once 
   he replied correctly"""

class QuizzMode(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color="#191919")
        self.root = root
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self.quizz_word_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=40, weight="bold"), wraplength=600,
                                             width=600, height=200)
        self.quizz_word_label.grid(row=0, column=0, pady=(50, 0), columnspan=3, rowspan=1)

        self.quizz_counter_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=25, weight="bold"))
        self.quizz_counter_label.grid(row=0, column=1, padx=5, pady=5, sticky="wn")

        # Making 4 possible position for the answer buttons and then mix them.
        self.buttons_params = mix([{'row': 3, 'column': 1, 'sticky': 'es', 'padx': (0, 20), 'pady': (100, 0)},
                                   {'row': 3, 'column': 2, 'sticky': 'ws', 'padx': 0, 'pady': (100, 0)},
                                   {'row': 4, 'column': 1, 'sticky': 'en', 'padx': (0, 20), 'pady': 20},
                                   {'row': 4, 'column': 2, 'sticky': 'wn', 'padx': 0, 'pady': 20}])

        self.correct_answer_button = ctk.CTkButton(self, width=330, height=100,
                                                   command=self.correct_answer_button_event,
                                                   font=ctk.CTkFont(size=30, weight="bold"))
        self.correct_answer_button.grid(**self.buttons_params[0])

        #Binding `wrong anwer buttons` in a loop
        self.wrong_buttons = []
        for i in range(1, 4):
            wrong_answer_button = ctk.CTkButton(self, width=330, height=100,
                                                font=ctk.CTkFont(size=30, weight="bold"))
            wrong_answer_button_event = partial(self.wrong_answer_button_event, button=wrong_answer_button)
            wrong_answer_button.configure(command=wrong_answer_button_event)
            wrong_answer_button.grid(**self.buttons_params[i])
            self.wrong_buttons.append(wrong_answer_button)

        self.test_len = self.word_pairs = self.word_pair = self.score = self.counter = self.subcounter = 0

    def start_quizz(self):
        words = get_text_from_file(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test')
        words = mix([i.split(' - ') for i in words])
        self.test_len = len(words)
        self.word_pairs = []
        for i in range(len(words)):
            temp = mix(words[:i] + words[i + 1:])
            self.word_pairs.append([words[i]] + temp[:3])
        self.word_pairs = iter(self.word_pairs)
        self.word_pair = next(self.word_pairs)
        self.score, self.counter = 0, 1
        self.quizz_word_label.configure(text=self.word_pair[0][1])
        self.quizz_counter_label.configure(text=f"{self.counter}/{self.test_len}")
        for i, button in enumerate((self.correct_answer_button, *self.wrong_buttons)):
            button.configure(fg_color='#1f538d', hover_color="#14375d", state='normal', text=self.word_pair[i][0])
        self.root.set_current_frame(self)

    def correct_answer_button_event(self):
        """ Is used in quizz mode"""
        self.score += 1 - self.subcounter
        self.counter += 1
        self.subcounter = 0
        if self.counter > self.test_len:
            # Test is over
            self.root.result_frame.result_label.configure(
                text=f"Your result:  {int(self.score)}/{self.test_len}\n{self.score * 100 // self.test_len}%")
            self.root.set_current_frame(self.root.result_frame)
            return
        shuffle(self.buttons_params)
        self.word_pair = next(self.word_pairs)
        for i, button in enumerate((self.correct_answer_button, *self.wrong_buttons)):
            button.grid_remove()
            button.configure(fg_color='#1f538d', hover_color="#14375d", state='normal', text=self.word_pair[i][0])
            # The correct answer is always in the same button, we only change its position
            button.grid(**self.buttons_params[i])
        self.quizz_word_label.configure(text=self.word_pair[0][1])
        self.quizz_counter_label.configure(text=f"{self.counter}/{self.test_len}")

    def wrong_answer_button_event(self, button: ctk.CTkButton):
        """ Is used in quizz mode"""
        if self.subcounter == 0:
            self.subcounter = 0.5
        elif self.subcounter == 0.5:
            self.subcounter = 1
        button.configure(state='disabled', fg_color='red')

