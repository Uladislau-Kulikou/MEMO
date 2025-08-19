from os import listdir

import customtkinter as ctk

from frames.CreateFile import CreateFile
from frames.QuizzMode import QuizzMode
from frames.ResultFrame import ResultFrame
from frames.Sidebar import SideBar
from frames.TestCreation import TestCreation
from frames.TestDeletion import TestDeletion
from frames.TestMode import TestMode
from frames.TestModeSelection import TestModeSelection
from frames.TestPreview import TestPreview
from frames.WordsAddition import WordsAddition
from helper_fn import *

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        check_oper_folder()
        self.title("MEMO")
        self.geometry("900x580")
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.test_creation_frame = TestCreation(self)
        self.create_file_frame = CreateFile(self)
        self.test_preview_frame = TestPreview(self)
        self.test_frame = TestMode(self)
        self.quizz_frame = QuizzMode(self)
        self.test_mode_selection_frame = TestModeSelection(self)
        self.words_addition_frame = WordsAddition(self)
        self.test_deletion_frame = TestDeletion(self)
        self.sidebar = SideBar(self)
        self.result_frame = ResultFrame(self)

        self.themes = []
        self.selected_theme = None
        self.update_theme_folders()

        self.tests = []
        self.selected_test = None
        if self.selected_theme:
            self.update_test_files()

        self.current_frame = None

        if not self.selected_theme:
            self.test_creation_frame.create_theme_button_event()
        else:
            self.test_preview_frame.show()

        self.sidebar.refresh()

    def update_theme_folders(self) -> None:
        self.themes = []
        self.selected_theme = None

        for folder in listdir(OPER_FOLDER):
            self.themes.append(folder)
        # if selected theme is None or doesn't exist anymore, and there is one found -> select it
        if self.selected_theme not in self.themes and self.themes:
            self.selected_theme = self.themes[0]
        else:
            self.selected_theme = None

    def update_test_files(self) -> None:
        self.tests = []
        self.selected_test = None
        if not self.selected_theme:
            return

        folder = f"{OPER_FOLDER}{self.selected_theme}"

        for filename in listdir(folder):
            if filename.endswith(".test"):
                test_name = filename[:-5:]  # removing file's extension from a name
                self.tests.append(test_name)
        # if selected test is None or doesn't exist anymore, and there is one found -> select it
        if self.tests:
            if self.selected_test not in self.tests:
                self.selected_test = self.tests[0]
        else:
            self.selected_test = None

    def set_current_frame(self, new_frame: ctk.CTkFrame):
        if self.current_frame:
            self.current_frame.grid_remove()
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")


if __name__ == "__main__":
    app = App()
    check_oper_folder()
    app.mainloop()
