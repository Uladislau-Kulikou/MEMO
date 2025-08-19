import customtkinter as ctk
from globals import OPER_FOLDER, ENCODING
from helper_fn import check_valid_input

"""A frame where we can add words to the test. It is used both when creating a test and pressing `Add_words` button"""

class WordsAddition(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color="#191919")
        self.root = root
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected_test_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=25, weight="bold"))
        self.selected_test_label.grid(row=0, column=0, sticky='wn', padx=(15, 0), pady=(15, 0))

        self.word_entry = ctk.CTkEntry(self, height=50, width=300, font=ctk.CTkFont(size=20),
                                       placeholder_text="word", justify=ctk.CENTER)
        self.word_entry.grid(row=1, column=0, sticky='e', padx=(0, 50))

        self.trans_entry = ctk.CTkEntry(self, height=50, width=300, font=ctk.CTkFont(size=20),
                                        placeholder_text="translation", justify=ctk.CENTER)
        self.trans_entry.grid(row=1, column=1, sticky='w')

        self.apply_button = ctk.CTkButton(self, command=self.add_word_to_test, text='Add words',
                                          height=40, font=ctk.CTkFont(size=20))
        self.apply_button.grid(row=3, pady=(20, 0), columnspan=2)

        self.save_test_button = ctk.CTkButton(self, command=self.save_button_event, text='Save',
                                              height=40, font=ctk.CTkFont(size=20))
        self.save_test_button.grid(row=5, column=1, pady=20, padx=20, sticky='se')

    def add_words_button_event(self):
        self.selected_test_label.configure(text=f'Selected test: {self.root.selected_test}')
        self.word_entry.configure(fg_color="#353638", border_color='#555560')
        self.trans_entry.configure(fg_color="#353638", border_color='#555560')
        self.root.sidebar.set('disabled')
        self.root.set_current_frame(self)

    def add_word_to_test(self):
        """ Gets output from `word_entry` and `trans_entry` and writes it into a file"""
        if not check_valid_input(self.trans_entry, self.word_entry):
            return
        with open(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test', 'a', encoding=ENCODING) as file:
            file.write(f'{self.word_entry.get()} - {self.trans_entry.get()}\n')
        self.trans_entry.delete(0, 'end')
        self.word_entry.delete(0, 'end')
        self.word_entry.focus_set()

    def save_button_event(self):
        self.root.sidebar.set('normal')
        self.root.sidebar.refresh()
        self.root.test_preview_frame.show()
