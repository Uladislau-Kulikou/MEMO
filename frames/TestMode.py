import customtkinter as ctk
from globals import OPER_FOLDER
from helper_fn import mix, get_text_from_file

"""Shows us a frame with a question and text_field for answer."""

class TestMode(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root,corner_radius=0, fg_color="#191919")
        self.root = root
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.test_counter_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=25, weight="bold"))
        self.test_counter_label.grid(row=0, padx=5, pady=5, sticky="wn")

        self.test_word_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=34, weight="bold"), wraplength=600,
                                            width=600, height=100)
        self.test_word_label.grid(row=1, padx=0, pady=(100, 0), columnspan=2, sticky='s')

        self.entry = ctk.CTkEntry(self, height=50, width=400, font=ctk.CTkFont(size=20), justify=ctk.CENTER)
        self.entry.grid(row=2, padx=0, pady=(0, 20))

        self.answer_button = ctk.CTkButton(self, width=150, height=35, text='Answer',
                                           font=ctk.CTkFont(size=20, weight="bold"), command=self.answer_button_event)
        self.answer_button.grid(row=3, sticky='n')

        self.correct_answer_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=34, weight="bold"),
                                                 text_color='green', wraplength=600, width=600, height=50)
        self.correct_answer_label.grid(row=4, pady=(50, 30), columnspan=2, sticky='n')

        self.word_pairs = self.word_iter = self.word_pair = self.score = self.counter = self.test_len = None
        self.show_test = self.is_answered = False

    def start_test(self):
        self.word_pairs = get_text_from_file(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test')
        self.word_pairs = mix([wrd.strip().split(' - ') for wrd in self.word_pairs])
        self.test_len = len(self.word_pairs)
        self.word_iter = iter(self.word_pairs)
        self.score, self.counter = 0, 1
        self.is_answered = False
        self.reset_test_items()
        self.root.set_current_frame(self)

    def answer_button_event(self):
        if self.is_answered:
            if self.counter > self.test_len:
                # Test is over
                self.root.result_frame.result_label.configure(
                    text=f"Your result:  {self.score}/{self.test_len}\n{self.score * 100 // self.test_len}%")
                self.root.set_current_frame(self.root.result_frame)
                return
            self.reset_test_items()
        else:
            self.counter += 1
            if self.entry.get().lower().strip() == self.word_pair[0].lower():
                self.score += 1
                self.entry.configure(fg_color="darkgreen", border_color='lightgreen')
            else:
                self.entry.configure(fg_color="darkred", border_color='red')
                self.correct_answer_label.configure(text=self.word_pair[0], text_color='green')
            self.answer_button.configure(text='Next')
        self.is_answered = not self.is_answered

    def reset_test_items(self):
        self.word_pair = next(self.word_iter)
        self.test_counter_label.configure(text=f"{self.counter}/{len(self.word_pairs)}")
        self.test_word_label.configure(text=self.word_pair[1])
        self.correct_answer_label.configure(text_color='#191919')
        self.entry.configure(fg_color="#353638", border_color='#555560')
        self.answer_button.configure(text='Answer')
        self.entry.delete(0, 'end')
        self.entry.focus_set()