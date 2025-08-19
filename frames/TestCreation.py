from os import makedirs

import customtkinter as ctk
from globals import OPER_FOLDER
from helper_fn import check_valid_input

"""A frame where we can create a new Theme/Test"""

class TestCreation(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color="#191919")
        self.root = root
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.test_name_label = ctk.CTkLabel(self, text=f"Type a name:",
                                            font=ctk.CTkFont(size=23, weight="bold"), corner_radius=0)
        self.test_name_label.grid(row=1, pady=15)

        self.filename_entry = ctk.CTkEntry(self, height=50, width=400, font=ctk.CTkFont(size=20),
                                           justify=ctk.CENTER)
        self.filename_entry.grid(row=2, pady=15)

        self.apply_file_name_button = ctk.CTkButton(self, command=self.create_test_file,
                                                    text='Create', height=40, font=ctk.CTkFont(size=20), width=100)
        self.apply_file_name_button.grid(row=3, pady=15)

        self.file_exists_warning = ctk.CTkLabel(self, text="File with this name already exists",
                                                font=ctk.CTkFont(size=18, weight="bold"), text_color='red')


    def create_theme_button_event(self):
        self.test_name_label.configure(text="Theme name:\n (Language you want to learn)")
        self.apply_file_name_button.configure(command=self.create_theme)
        self.root.set_current_frame(self)
        self.file_exists_warning.grid_remove()
        self.filename_entry.focus_set()

    def create_theme(self):
        theme_name = self.filename_entry.get().strip()
        if theme_name in self.root.themes:
            self.filename_entry.configure(fg_color="darkred", border_color='red')
            self.file_exists_warning.grid(column=0, row=4, pady=20, sticky='s')
            return
        elif not check_valid_input(self.filename_entry, exclude=r'/\:*?"|<>'):
            return
        self.filename_entry.delete(0, 'end')
        makedirs(OPER_FOLDER + theme_name)
        self.root.update_theme_folders()
        self.root.selected_theme = theme_name
        self.root.update_test_files()
        self.create_test_button_event()
        self.root.sidebar.refresh()

    def create_test_button_event(self):
        self.test_name_label.configure(text="Test name:")
        self.apply_file_name_button.configure(command=self.create_test_file)
        self.root.set_current_frame(self)
        self.file_exists_warning.grid_remove()
        self.filename_entry.focus_set()

    def create_test_file(self):
        test_name = self.filename_entry.get().strip()
        if test_name in self.root.tests:
            self.filename_entry.configure(fg_color="darkred", border_color='red')
            self.file_exists_warning.grid(column=0, row=4, pady=20, sticky='s')
            return
        elif not check_valid_input(self.filename_entry, exclude=r'/\:*?"|<>'):
            return
        self.filename_entry.delete(0, 'end')
        open(rf'{OPER_FOLDER}{self.root.selected_theme}\{test_name}.test', 'x')  # Creates new file
        self.root.update_test_files()
        self.root.selected_test = test_name
        self.root.sidebar.refresh()
        self.root.words_addition_frame.add_words_button_event()
