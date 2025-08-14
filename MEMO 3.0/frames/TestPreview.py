import customtkinter as ctk
from ScrollableLabel import ScrollableLabel

from globals import OPER_FOLDER
from helper_fn import get_text_from_file


class TestPreview(ctk.CTkFrame):
    def __init__(self, root):
        self.root = root
        super().__init__(root, fg_color="#1a1a1a", corner_radius=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.words_label = ScrollableLabel(self, label_fg_color='#1a1a1a', fg_color="#1a1a1a")
        self.words_label.grid(rowspan=2, columnspan=2, sticky='nsew')

        self.word_count_prewiew_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=16, weight="bold"),
                                                     text_color="#5a5b5c", text='-')
        self.word_count_prewiew_label.grid(row=0, column=0, sticky='wn', padx=(5, 0), pady=(5, 0))

    def show(self):
        self.root.set_current_frame(self)
        if not self.root.selected_test:
            self.words_label.clear()
            self.word_count_prewiew_label.configure(text='Test does not exist', text_color='#5a5b5c')
            return

        text = get_text_from_file(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test')
        text_len = len(text)
        self.words_label.clear()
        for line in text:
            self.words_label.add_item(line)

        self.word_count_prewiew_label.configure(text=f"{text_len} word{'' if text_len == 1 else 's'}")

        if text_len == 0:
            self.word_count_prewiew_label.configure(text_color='red')
        elif text_len < 4:
            self.word_count_prewiew_label.configure(text_color='orange')
        else:
            self.word_count_prewiew_label.configure(text_color='white')