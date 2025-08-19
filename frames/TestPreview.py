import customtkinter as ctk
from ScrollableLabel import ScrollableLabel

from globals import OPER_FOLDER
from helper_fn import get_text_from_file

""" This is the default frame that shows us what the selected test contains in a scrollable format.
    If there is no theme found - we go to theme_creation_frame (this logic is not handled here)
    If there is no test found - the `word counter` just says 'Test doesn't exits' """

class TestPreview(ctk.CTkFrame):
    def __init__(self, root):
        self.root = root
        super().__init__(root, fg_color="#1a1a1a", corner_radius=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.words_label = ScrollableLabel(self, label_fg_color='#1a1a1a', fg_color="#1a1a1a")
        self.words_label.grid(rowspan=2, columnspan=2, sticky='nsew')

        self.word_count_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=16, weight="bold"),
                                             text_color="#5a5b5c", text='-')
        self.word_count_label.grid(row=0, column=0, sticky='wn', padx=(5, 0), pady=(5, 0))
        self.word_count_suggestion = ctk.CTkLabel(self, font=ctk.CTkFont(size=15, weight="bold"),
                                                     text_color="#2b2d30", text='(Consider splitting the test)')

    def show(self):
        self.root.set_current_frame(self)
        if not self.root.selected_test:
            self.words_label.clear()
            self.word_count_label.configure(text='Test does not exist', text_color='#5a5b5c')
            return

        self.word_count_suggestion.grid_remove()
        text = get_text_from_file(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test')
        word_count = len(text)
        self.words_label.clear()
        for line in text:
            self.words_label.add_item(line)

        self.word_count_label.configure(text=f"{word_count} word{'' if word_count == 1 else 's'}")

        if word_count == 0:
            self.word_count_label.configure(text_color='red') # No mode is available
        elif word_count < 4:
            self.word_count_label.configure(text_color='orange') # Quizz mode is not available
        else:
            self.word_count_label.configure(text_color='white') # OK\

        if word_count > 30:
            self.word_count_suggestion.grid(row=0, column=1, sticky='wn', padx=(15, 0), pady=(5, 0))