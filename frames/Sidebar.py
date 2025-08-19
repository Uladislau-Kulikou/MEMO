from os import startfile
from subprocess import Popen

import customtkinter as ctk
from globals import OPER_FOLDER
from helper_fn import validate_testfile


class SideBar(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color='#202020')
        self.root = root
        self.grid(rowspan=10, sticky="nsew")
        self.grid_rowconfigure(9, weight=1)

        self.start_test_button = ctk.CTkButton(self, text='📁', command=self.open_source, font=ctk.CTkFont(size=20),
                                               fg_color='#202020', text_color='#858585', width=10, height=20, hover_color='#474747')
        self.start_test_button.grid(row=0, padx=0, pady=0, sticky='wn')

        self.theme_label = ctk.CTkLabel(self, text="Theme: ", font=ctk.CTkFont(size=20, weight="bold"))
        self.theme_label.grid(row=0, pady=(20, 0))

        self.themes_combobox = ctk.CTkOptionMenu(self, command=self.theme_option_menu_event, anchor='s',
                                                 font=ctk.CTkFont(size=15), values=["No theme found"])
        self.themes_combobox.grid(row=1, pady=10)

        self.tests_label = ctk.CTkLabel(self, text="Test: ", font=ctk.CTkFont(size=20, weight="bold"))
        self.tests_label.grid(row=2, pady=(20, 0))

        self.tests_combobox = ctk.CTkOptionMenu(self, command=self.test_option_menu_event, anchor='s',
                                                font=ctk.CTkFont(size=15), values=["No test found"])
        self.tests_combobox.grid(row=3, pady=(0, 10))

        self.start_test_button = ctk.CTkButton(self, text='Start test', command=root.test_mode_selection_frame.select_test_mode,
                                               font=ctk.CTkFont(size=15))
        self.start_test_button.grid(row=5, pady=(40, 10))

        self.edit_test_button = ctk.CTkButton(self, text='Edit test', command=self.edit_test,
                                              font=ctk.CTkFont(size=15))
        self.edit_test_button.grid(row=6, pady=10)

        self.add_words_button = ctk.CTkButton(self, text='Add words', command=root.words_addition_frame.add_words_button_event,
                                              font=ctk.CTkFont(size=15))
        self.add_words_button.grid(row=7, pady=10)

        self.delete_test_button = ctk.CTkButton(self, text='Delete',
                                                command=root.test_deletion_frame.delete_test_button_event, font=ctk.CTkFont(size=15),
                                                fg_color="#ad1d1d", hover_color="darkred")
        self.delete_test_button.grid(row=8, pady=10)

        self.create_button = ctk.CTkButton(self, text='Create', width=180, corner_radius=0,
                                           command=root.create_file_frame.create_button_event, font=ctk.CTkFont(size=15))
        self.create_button.grid(row=10)

    def set(self, state: str, *exception) -> None:
        """Disables or enables entities in sidebar with given exeptions"""
        for item in self.get_entities():
            if item not in exception:
                item.configure(state=state)

    def get_entities(self):
        """Returns sidebar entities."""
        # Some objects are being recreated so makig a list in advance won't work
        return (self.themes_combobox, self.tests_combobox, self.start_test_button, self.edit_test_button,
                   self.add_words_button, self.delete_test_button, self.create_button)

    def refresh(self):
        """Refreshes comboboxes. Used when any changes were applied to test files"""
        self.themes_combobox.configure(values=self.root.themes or ["No theme found"])
        self.themes_combobox.set(self.root.selected_theme)

        self.tests_combobox.configure(values=self.root.tests or ["No test found"])
        self.tests_combobox.set(self.root.selected_test)

        if self.root.selected_test:
            self.set('normal')
        else:
            self.set('disabled', self.create_button)

        if self.root.selected_theme:
            state = 'normal'
        else:
            state = 'disabled'
        self.themes_combobox.configure(state=state)
        self.delete_test_button.configure(state=state)

    def theme_option_menu_event(self, new_theme):
        self.root.selected_theme = new_theme
        self.root.update_test_files()
        self.refresh()
        self.root.test_preview_frame.show()

    def test_option_menu_event(self, new_test):
        self.root.selected_test = new_test
        validate_testfile(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test')
        self.root.test_preview_frame.show()


    def edit_test(self):
        """Opens selected test file in Notepad"""
        Popen(rf"notepad {OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test")


    @staticmethod
    def open_source():
        startfile(OPER_FOLDER)
