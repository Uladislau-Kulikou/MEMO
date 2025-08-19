import customtkinter as ctk
from globals import OPER_FOLDER
from helper_fn import validate_testfile, get_text_from_file

"""Frame that asks whether we want to pass a test or a quizz. Here all the preaparations are being done for those
    Like formatting files correctly. Shows us warnings if the test is too small"""

class TestModeSelection(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color="#191919")
        self.root = root
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.selection_info_label = ctk.CTkLabel(self, text="Select mode:",
                                                 font=ctk.CTkFont(size=40, weight="bold"))
        self.selection_info_label.grid(row=0, column=0, pady=(100, 100), padx=(0, 0), columnspan=2, sticky='sew')

        self.select_test_mode_button = ctk.CTkButton(self, command=root.test_frame.start_test,
                                                     text='Test', height=60, font=ctk.CTkFont(size=30))
        self.select_test_mode_button.grid(row=1, column=0, sticky='nse', padx=(50, 50))

        self.select_quizz_mode_button = ctk.CTkButton(self, command=root.quizz_frame.start_quizz,
                                                      text='Quizz', height=60, font=ctk.CTkFont(size=30))
        self.select_quizz_mode_button.grid(row=1, column=1, sticky='nsw', padx=(50, 50))

        self.empty_file_warning = ctk.CTkLabel(self,
                                               text="Selected test is empty.\n Test mode is not available.",
                                               font=ctk.CTkFont(size=18, weight="bold"), text_color='red')
        self.too_few_words_warning = ctk.CTkLabel(self,
                                                  text="Selected test is too small.\n Quizz mode is not available.",
                                                  font=ctk.CTkFont(size=18, weight="bold"), text_color='red')

    def select_test_mode(self):
        validate_testfile(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test')
        self.root.sidebar.start_test_button.configure(text="Exit test", fg_color="red", hover_color="darkred")
        self.root.test_frame.show_test = not self.root.test_frame.show_test

        if self.root.test_frame.show_test:
            self.root.sidebar.set('disabled', self.root.sidebar.start_test_button)
            self.root.set_current_frame(self)
            test_len = len(get_text_from_file(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test'))
            # Removing possible warnings that might be on the frame on previous call
            self.empty_file_warning.grid_remove()
            self.too_few_words_warning.grid_remove()

            if test_len == 0:
                # Test mode is not available
                self.empty_file_warning.grid(column=0, row=2, pady=40, padx=(0, 30), sticky='en')
                self.select_test_mode_button.configure(state='disabled')
            else:
                # Even if there is 1 only word, we can do a test
                self.select_test_mode_button.configure(state='normal')

            if test_len < 4:
                # A Quizz question needs at least 4 possible answers
                self.too_few_words_warning.grid(column=1, row=2, pady=40, padx=(30, 0), sticky='wn')
                self.select_quizz_mode_button.configure(state='disabled')
            else:
                self.select_quizz_mode_button.configure(state='normal')
        else:
            self.root.sidebar.set('normal')
            self.root.sidebar.start_test_button.configure(text='Start test', fg_color='#1f538d', hover_color="#14375d")
            self.root.test_preview_frame.show()