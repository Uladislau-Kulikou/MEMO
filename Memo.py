import os
from functools import partial
from itertools import takewhile
from os import remove, makedirs, listdir
from random import shuffle
from subprocess import Popen

import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
# ctk.set_widget_scaling(2)

ENCODING = 'UTF-8'
OPER_FOLDER = os.path.join(os.getenv('LOCALAPPDATA'), "MEMO\\")
print(OPER_FOLDER)

class ScrollableLabel(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.label_list = []
        self.length = 0

    def add_item(self, item):
        label = ctk.CTkLabel(self, text=item, font=ctk.CTkFont(size=25), wraplength=500)
        label.grid(row=self.length, sticky='nsew', pady=(50 if self.length == 0 else 0, 0))
        self.label_list.append(label)
        self.length += 1

    def clear(self):
        for label in self.label_list:
            label.destroy()
        del self.label_list[:]
        self.length = 0


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        check_oper_folder()
        self.title("MEMO")
        # self.resizable(False, False)
        self.geometry("900x580")
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)
        # ---------------------- Sidebar frame ------------------------ #
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)

        self.start_test_button = ctk.CTkButton(self.sidebar_frame, text='📁', command=self.open_source,font=ctk.CTkFont(size=20,),
                                               fg_color='#212121', text_color='#858585', width=15, height=10, anchor='w', hover_color='#474747')
        self.start_test_button.grid(row=0, padx=0, pady=0, sticky='wn')

        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Theme: ", font=ctk.CTkFont(size=20, weight="bold"))
        self.theme_label.grid(row=0, pady=(20, 0))

        self.themes_combobox = ctk.CTkOptionMenu(self.sidebar_frame, command=self.theme_option_menu_event, anchor='s',
                                                font=ctk.CTkFont(size=15))
        self.themes_combobox.grid(row=1, pady=10)

        self.tests_label = ctk.CTkLabel(self.sidebar_frame, text="Test: ", font=ctk.CTkFont(size=20, weight="bold"))
        self.tests_label.grid(row=2, pady=(20, 0))

        self.tests_combobox = ctk.CTkOptionMenu(self.sidebar_frame, command=self.test_option_menu_event, anchor='s',
                                                font=ctk.CTkFont(size=15))
        self.tests_combobox.grid(row=3, pady=(0, 10))

        self.start_test_button = ctk.CTkButton(self.sidebar_frame, text='Start test', command=self.select_test_mode,
                                               font=ctk.CTkFont(size=15))
        self.start_test_button.grid(row=5, pady=(40,10))

        self.edit_test_button = ctk.CTkButton(self.sidebar_frame, text='Edit test', command=self.edit_test,
                                              font=ctk.CTkFont(size=15))
        self.edit_test_button.grid(row=6, pady=10)

        self.add_words_button = ctk.CTkButton(self.sidebar_frame, text='Add words', command=self.add_words_button_event,
                                              font=ctk.CTkFont(size=15))
        self.add_words_button.grid(row=7, pady=10)

        self.delete_test_button = ctk.CTkButton(self.sidebar_frame, text='Delete',
                                                command=self.delete_test_button_event, font=ctk.CTkFont(size=15),
                                                fg_color="#ad1d1d", hover_color="darkred")
        self.delete_test_button.grid(row=8, pady=10)

        self.create_button = ctk.CTkButton(self.sidebar_frame, text='Create', width=180, corner_radius=0,
                                           command=self.create_button_event, font=ctk.CTkFont(size=15))
        self.create_button.grid(row=10)

        # --------------------------- Create frame ---------------------------#
        self.create_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.create_frame.grid_columnconfigure(0, weight=1)
        self.create_frame.grid_columnconfigure(1, weight=1)
        self.create_frame.grid_rowconfigure(0, weight=1)
        self.create_frame.grid_rowconfigure(2, weight=1)

        self.create_theme_button = ctk.CTkButton(self.create_frame, command=self.create_theme_button_event,
                                                 text='New theme', height=60, font=ctk.CTkFont(size=30))
        self.create_theme_button.grid(row=1, column=0, sticky='nse', padx=(50, 50))

        self.create_test_button = ctk.CTkButton(self.create_frame, command=self.create_test_button_event,
                                                     text='New test', height=60, font=ctk.CTkFont(size=30))
        self.create_test_button.grid(row=1, column=1, sticky='nsw', padx=(50, 50))
        # ------------------------ test preview frame ----------------------- #
        self.test_preview_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=0)
        self.test_preview_frame.grid_columnconfigure(1, weight=1)
        self.test_preview_frame.grid_rowconfigure(1, weight=1)

        self.words_label = ScrollableLabel(self.test_preview_frame, label_fg_color='#1a1a1a', fg_color="#1a1a1a")
        self.words_label.grid(rowspan=2, columnspan=2, sticky='nsew')

        self.word_count_prewiew_label = ctk.CTkLabel(self.test_preview_frame, font=ctk.CTkFont(size=16, weight="bold"),
                                                     text_color="#5a5b5c", text='-')
        self.word_count_prewiew_label.grid(row=0, column=0, sticky='wn', padx=(5, 0), pady=(5, 0))
        # --------------------- test mode selection frame ------------------- #
        self.test_mode_selection_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.test_mode_selection_frame.grid_rowconfigure(0, weight=1)
        self.test_mode_selection_frame.grid_rowconfigure(2, weight=1)
        self.test_mode_selection_frame.grid_columnconfigure(0, weight=1)
        self.test_mode_selection_frame.grid_columnconfigure(1, weight=1)

        self.selection_info_label = ctk.CTkLabel(self.test_mode_selection_frame, text="Select mode:",
                                                 font=ctk.CTkFont(size=40, weight="bold"))
        self.selection_info_label.grid(row=0, column=0, pady=(100, 100), padx=(0, 0), columnspan=2, sticky='sew')

        self.select_test_mode_button = ctk.CTkButton(self.test_mode_selection_frame, command=self.start_test,
                                                     text='Test', height=60, font=ctk.CTkFont(size=30))
        self.select_test_mode_button.grid(row=1, column=0, sticky='nse', padx=(50, 50))

        self.select_quizz_mode_button = ctk.CTkButton(self.test_mode_selection_frame, command=self.start_quizz,
                                                      text='Quizz', height=60, font=ctk.CTkFont(size=30))
        self.select_quizz_mode_button.grid(row=1, column=1, sticky='nsw', padx=(50, 50))

        self.empty_file_warning = ctk.CTkLabel(self.test_mode_selection_frame,
                                               text="Selected test is empty.\n Test mode is not available.",
                                               font=ctk.CTkFont(size=18, weight="bold"), text_color='red')
        self.too_few_words_warning = ctk.CTkLabel(self.test_mode_selection_frame,
                                                  text="Selected test is too small.\n Quizz mode is not available.",
                                                  font=ctk.CTkFont(size=18, weight="bold"), text_color='red')
        # ---------------------- test creation frame ------------------- #
        self.create_test_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.create_test_frame.grid_columnconfigure(0, weight=1)
        self.create_test_frame.grid_rowconfigure(0, weight=1)
        self.create_test_frame.grid_rowconfigure(4, weight=1)

        self.test_name_label = ctk.CTkLabel(self.create_test_frame, text=f"Type a name:",
                                            font=ctk.CTkFont(size=23, weight="bold"), corner_radius=0)
        self.test_name_label.grid(row=1, pady=15)

        self.filename_entry = ctk.CTkEntry(self.create_test_frame, height=50, width=400, font=ctk.CTkFont(size=20),
                                           justify=ctk.CENTER)
        self.filename_entry.grid(row=2, pady=15)

        self.apply_file_name_button = ctk.CTkButton(self.create_test_frame, command=self.create_test_file,
                                                    text='Create', height=40, font=ctk.CTkFont(size=20), width=100)
        self.apply_file_name_button.grid(row=3, pady=15)

        self.file_exists_warning = ctk.CTkLabel(self.create_test_frame, text="File with this name already exists",
                                                font=ctk.CTkFont(size=18, weight="bold"), text_color='red')

        # -------------------- words addition frame  ---------------------- #
        self.add_words_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.add_words_frame.grid_columnconfigure(0, weight=1)
        self.add_words_frame.grid_columnconfigure(1, weight=1)
        self.add_words_frame.grid_rowconfigure(5, weight=1)
        self.add_words_frame.grid_rowconfigure(0, weight=1)

        self.selected_test_label = ctk.CTkLabel(self.add_words_frame, font=ctk.CTkFont(size=25, weight="bold"))
        self.selected_test_label.grid(row=0, column=0, sticky='wn', padx=(15, 0), pady=(15, 0))

        self.word_entry = ctk.CTkEntry(self.add_words_frame, height=50, width=300, font=ctk.CTkFont(size=20),
                                       placeholder_text="word", justify=ctk.CENTER)
        self.word_entry.grid(row=1, column=0, sticky='e', padx=(0, 50))

        self.trans_entry = ctk.CTkEntry(self.add_words_frame, height=50, width=300, font=ctk.CTkFont(size=20),
                                        placeholder_text="translation", justify=ctk.CENTER)
        self.trans_entry.grid(row=1, column=1, sticky='w')

        self.apply_button = ctk.CTkButton(self.add_words_frame, command=self.add_word_to_test, text='Add words',
                                          height=40, font=ctk.CTkFont(size=20))
        self.apply_button.grid(row=3, pady=(20, 0), columnspan=2)

        self.save_test_button = ctk.CTkButton(self.add_words_frame, command=self.save_button_event, text='Save',
                                              height=40, font=ctk.CTkFont(size=20))
        self.save_test_button.grid(row=5, column=1, pady=20, padx=20, sticky='se')
        # ---------------------- test deletion frame -------------------- #
        self.deletion_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.deletion_frame.columnconfigure(0, weight=1)
        self.deletion_frame.columnconfigure(1, weight=1)
        self.deletion_frame.rowconfigure(0, weight=1)
        self.deletion_frame.rowconfigure(3, weight=1)

        self.confirmation_label = ctk.CTkLabel(self.deletion_frame, font=ctk.CTkFont(size=34, weight="bold"),
                                               wraplength=620, justify=ctk.CENTER)
        self.confirmation_label.grid(row=1, columnspan=2, pady=(0, 100))

        self.decline_button = ctk.CTkButton(self.deletion_frame, text='No', command=self.decline_deletion_event,
                                            height=50, font=ctk.CTkFont(size=20), width=100)
        self.decline_button.grid(row=2, column=0, padx=(0, 50), sticky='e')

        self.accept_button = ctk.CTkButton(self.deletion_frame, text='Yes', command=self.accept_deletion_event,
                                           height=50, font=ctk.CTkFont(size=20), width=100, fg_color="red",
                                           hover_color="darkred")
        self.accept_button.grid(row=2, column=1, padx=(50, 0), sticky='w')
        # ------------------------ test mode frame --------------------- #
        self.test_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.test_frame.grid_columnconfigure(0, weight=1)
        self.test_frame.grid_rowconfigure(0, weight=1)
        self.test_frame.grid_rowconfigure(4, weight=1)

        self.test_counter_label = ctk.CTkLabel(self.test_frame, font=ctk.CTkFont(size=25, weight="bold"))
        self.test_counter_label.grid(row=0, padx=5, pady=5, sticky="wn")

        self.test_word_label = ctk.CTkLabel(self.test_frame, font=ctk.CTkFont(size=34, weight="bold"), wraplength=600,
                                            width=600, height=100)
        self.test_word_label.grid(row=1, padx=0, pady=(100, 0), columnspan=2, sticky='s')

        self.entry = ctk.CTkEntry(self.test_frame, height=50, width=400, font=ctk.CTkFont(size=20), justify=ctk.CENTER)
        self.entry.grid(row=2, padx=0, pady=(0, 20))

        self.answer_button = ctk.CTkButton(self.test_frame, width=150, height=35, text='Answer',
                                           font=ctk.CTkFont(size=20, weight="bold"), command=self.answer_button_event)
        self.answer_button.grid(row=3, sticky='n')

        self.correct_answer_label = ctk.CTkLabel(self.test_frame, font=ctk.CTkFont(size=34, weight="bold"),
                                                 text_color='green', wraplength=600, width=600, height=50)
        self.correct_answer_label.grid(row=4, pady=(50, 30), columnspan=2, sticky='n')
        # ---------------------------- test result frame --------------- #
        self.test_score_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.test_score_frame.columnconfigure(0, weight=1)
        self.test_score_frame.rowconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(self.test_score_frame, font=ctk.CTkFont(size=34, weight="bold"),
                                         corner_radius=0)
        self.result_label.grid(row=0, column=0, sticky="nsew")
        # --------------------------- quizz frame ---------------------- #
        self.quizz_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#191919")
        self.quizz_frame.columnconfigure(1, weight=1)
        self.quizz_frame.columnconfigure(2, weight=1)
        self.quizz_frame.rowconfigure(0, weight=1)
        self.quizz_frame.rowconfigure(4, weight=1)

        self.buttons_params = mix([{'row': 3, 'column': 1, 'sticky': 'es', 'padx': (0, 20), 'pady': (100, 0)},
                                   {'row': 3, 'column': 2, 'sticky': 'ws', 'padx': 0, 'pady': (100, 0)},
                                   {'row': 4, 'column': 1, 'sticky': 'en', 'padx': (0, 20), 'pady': 20},
                                   {'row': 4, 'column': 2, 'sticky': 'wn', 'padx': 0, 'pady': 20}])

        self.quizz_word_label = ctk.CTkLabel(self.quizz_frame, font=ctk.CTkFont(size=40, weight="bold"), wraplength=600,
                                             width=600, height=200)
        self.quizz_word_label.grid(row=0, column=0, pady=(50, 0), columnspan=3, rowspan=1)

        self.quizz_counter_label = ctk.CTkLabel(self.quizz_frame, font=ctk.CTkFont(size=25, weight="bold"))
        self.quizz_counter_label.grid(row=0, column=1, padx=5, pady=5, sticky="wn")

        self.correct_answer_button = ctk.CTkButton(self.quizz_frame, width=330, height=100,
                                                   command=self.correct_answer_button_event,
                                                   font=ctk.CTkFont(size=30, weight="bold"))
        self.correct_answer_button.grid(**self.buttons_params[0])

        self.wrong_buttons = []
        for i in range(1, 4):
            wrong_answer_button = ctk.CTkButton(self.quizz_frame, width=330, height=100,
                                                font=ctk.CTkFont(size=30, weight="bold"))
            wrong_answer_button_event = partial(self.wrong_answer_button_event, button=wrong_answer_button)
            wrong_answer_button.configure(command=wrong_answer_button_event)
            wrong_answer_button.grid(**self.buttons_params[i])
            self.wrong_buttons.append(wrong_answer_button)
        # -------------------------- variables ------------------------- #
        self.themes = []
        self.selected_theme = None
        self.update_theme_folders()

        self.tests = []
        self.selected_test = None
        if self.selected_theme:
            self.update_test_files()

        self.current_frame = None
        self.show_test = self.is_answered = False  # tells if we need to start or exit test. Button changes it's functionality
        # Declaring variables to make them visible in other methods
        self.word_pairs = self.word_iter = self.word_pair = self.score = self.counter = self.test_len = None
        self.subcounter = 0

        if not self.selected_theme:
            self.create_theme_button_event()
        else:
            self.show_test_preview()

    def open_source(self):
        os.startfile(OPER_FOLDER)

    def select_test_mode(self):
        validate_testfile(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test')
        self.start_test_button.configure(text="Exit test", fg_color="red", hover_color="darkred")
        self.show_test = not self.show_test

        if self.show_test:
            self.set_sidebar('disabled', self.start_test_button)
            self.set_current_frame(self.test_mode_selection_frame)
            test_len = len(get_text_from_file(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test'))
            self.empty_file_warning.grid_remove()
            self.too_few_words_warning.grid_remove()

            if test_len == 0:
                self.empty_file_warning.grid(column=0, row=2, pady=40, padx=(0, 30), sticky='en')
                self.select_test_mode_button.configure(state='disabled')
            else:
                self.select_test_mode_button.configure(state='normal')

            if test_len < 4:
                self.too_few_words_warning.grid(column=1, row=2, pady=40, padx=(30, 0), sticky='wn')
                self.select_quizz_mode_button.configure(state='disabled')
            else:
                self.select_quizz_mode_button.configure(state='normal')
        else:
            self.set_sidebar('normal')
            self.start_test_button.configure(text='Start test', fg_color='#1f538d', hover_color="#14375d")
            self.show_test_preview()

    def create_button_event(self):
        if not self.selected_theme:
            self.create_theme_button_event()
            return
        self.set_current_frame(self.create_frame)

    def create_theme_button_event(self):
        self.test_name_label.configure(text="Theme name:\n (Language you want to learn)")
        self.apply_file_name_button.configure(command=self.create_theme)
        self.set_current_frame(self.create_test_frame)
        self.file_exists_warning.grid_remove()
        self.filename_entry.focus_set()
        
    def create_theme(self):
        theme_name = self.filename_entry.get().strip()
        if theme_name in self.themes:
            self.filename_entry.configure(fg_color="darkred", border_color='red')
            self.file_exists_warning.grid(column=0, row=4, pady=20, sticky='s')
            return
        elif not check_valid_input(self.filename_entry, exclude=r'/\:*?"|<>'):
            return
        self.filename_entry.delete(0, 'end')
        makedirs(OPER_FOLDER + theme_name)
        self.update_theme_folders()
        self.selected_theme = theme_name
        self.update_test_files()
        self.create_test_button_event()
        self.update_sidebar()
        
    def create_test_button_event(self):
        self.test_name_label.configure(text="Test name:")
        self.apply_file_name_button.configure(command=self.create_test_file)
        self.set_current_frame(self.create_test_frame)
        self.file_exists_warning.grid_remove()
        self.filename_entry.focus_set()

    def create_test_file(self):
        test_name = self.filename_entry.get().strip()
        if test_name in self.tests:
            self.filename_entry.configure(fg_color="darkred", border_color='red')
            self.file_exists_warning.grid(column=0, row=4, pady=20, sticky='s')
            return
        elif not check_valid_input(self.filename_entry, exclude=r'/\:*?"|<>'):
            return
        self.filename_entry.delete(0, 'end')
        open(rf'{OPER_FOLDER}{self.selected_theme}\{test_name}.test', 'x')  # Creates new file
        self.update_test_files()
        self.selected_test = test_name
        self.add_words_button_event()

    def add_words_button_event(self):
        self.selected_test_label.configure(text=f'Selected test: {self.selected_test}')
        self.word_entry.configure(fg_color="#353638", border_color='#555560')
        self.trans_entry.configure(fg_color="#353638", border_color='#555560')
        self.set_sidebar('disabled')
        self.set_current_frame(self.add_words_frame)

    def add_word_to_test(self):
        """ Gets output from `word_entry` and `trans_entry` and writes it into a file"""
        if not check_valid_input(self.trans_entry, self.word_entry):
            return
        with open(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test', 'a', encoding=ENCODING) as file:
            file.write(f'{self.word_entry.get()} - {self.trans_entry.get()}\n')
        self.trans_entry.delete(0, 'end')
        self.word_entry.delete(0, 'end')
        self.word_entry.focus_set()

    def save_button_event(self):
        self.set_sidebar('normal')
        self.update_sidebar()
        self.show_test_preview()

    def show_test_preview(self):
        self.set_current_frame(self.test_preview_frame)
        if not self.selected_test:
            self.words_label.clear()
            self.word_count_prewiew_label.configure(text='Test does not exist', text_color='#5a5b5c')
            return

        text = get_text_from_file(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test')
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

    def set_current_frame(self, new_frame: ctk.CTkFrame):
        if self.current_frame:
            self.current_frame.grid_remove()
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")

    def edit_test(self):
        """Opens selected test file in Notepad"""
        Popen(rf"notepad {OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test")

    def delete_test_button_event(self):
        self.set_sidebar('disabled')
        if self.tests:
            text = f'Are you sure you want to delete test "{self.selected_test}" from "{self.selected_theme}"?'
        else:
            text = f'Are you sure you want to delete theme "{self.selected_theme}"?'
        self.confirmation_label.configure(text=text)
        self.set_current_frame(self.deletion_frame)

    def decline_deletion_event(self):
        self.set_sidebar('normal')
        self.show_test_preview()

    def accept_deletion_event(self):
        self.set_sidebar('normal')
        if self.tests:
            remove(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test')  # Deletes file
        else:
            os.rmdir(rf'{OPER_FOLDER}{self.selected_theme}')
            self.update_theme_folders()
        self.update_test_files()
        self.update_sidebar()
        self.show_test_preview()

    def update_sidebar(self):
        self.themes_combobox.destroy()  # Option menu has to be recreated, otherwise it will contain the previous obsolete value
        self.themes_combobox = ctk.CTkOptionMenu(self.sidebar_frame, values=self.themes or ["No theme found"],
                                                command=self.theme_option_menu_event, anchor='s',
                                                font=ctk.CTkFont(size=15))
        self.themes_combobox.grid(row=1, pady=10)
        self.themes_combobox.set(self.selected_theme)

        self.tests_combobox.destroy()  # Option menu has to be recreated, otherwise it will contain the previous obsolete value
        self.tests_combobox = ctk.CTkOptionMenu(self.sidebar_frame, values=self.tests or ["No test found"],
                                                command=self.test_option_menu_event, anchor='s',
                                                font=ctk.CTkFont(size=15))
        self.tests_combobox.grid(row=3, pady=10)
        self.tests_combobox.set(self.selected_test)

        if self.selected_test:
            self.set_sidebar('normal')
        else:
            self.set_sidebar('disabled', self.create_button)

        if self.selected_theme:
            state = 'normal'
        else:
            state = 'disabled'
        self.themes_combobox.configure(state=state)
        self.delete_test_button.configure(state=state)

    def reset_test_items(self):
        self.word_pair = next(self.word_iter)
        self.test_counter_label.configure(text=f"{self.counter}/{len(self.word_pairs)}")
        self.test_word_label.configure(text=self.word_pair[1])
        self.correct_answer_label.configure(text_color='#191919')
        self.entry.configure(fg_color="#353638", border_color='#555560')
        self.answer_button.configure(text='Answer')
        self.entry.delete(0, 'end')
        self.entry.focus_set()

    def start_test(self):
        self.word_pairs = get_text_from_file(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test')
        self.word_pairs = mix([wrd.strip().split(' - ') for wrd in self.word_pairs])
        self.test_len = len(self.word_pairs)
        self.word_iter = iter(self.word_pairs)
        self.score, self.counter = 0, 1
        self.is_answered = False
        self.reset_test_items()
        self.set_current_frame(self.test_frame)

    def answer_button_event(self):
        if self.is_answered:
            if self.counter > self.test_len:
                # Test is over
                self.result_label.configure(
                    text=f"Your result:  {self.score}/{self.test_len}\n{self.score * 100 // self.test_len}%")
                self.set_current_frame(self.test_score_frame)
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

    def start_quizz(self):
        words = get_text_from_file(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test')
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
        self.set_current_frame(self.quizz_frame)

    def correct_answer_button_event(self):
        """ Is used in quizz """
        self.score += 1 - self.subcounter
        self.counter += 1
        self.subcounter = 0
        if self.counter > self.test_len:
            # Test is over
            self.result_label.configure(
                text=f"Your result:  {int(self.score)}/{self.test_len}\n{self.score * 100 // self.test_len}%")
            self.set_current_frame(self.test_score_frame)
            return
        shuffle(self.buttons_params)
        self.word_pair = next(self.word_pairs)
        for i, button in enumerate((self.correct_answer_button, *self.wrong_buttons)):
            button.grid_remove()
            button.configure(fg_color='#1f538d', hover_color="#14375d", state='normal', text=self.word_pair[i][0])
            # The correct answer is always in the same button, we only change it's position
            button.grid(**self.buttons_params[i])
        self.quizz_word_label.configure(text=self.word_pair[0][1])
        self.quizz_counter_label.configure(text=f"{self.counter}/{self.test_len}")

    def wrong_answer_button_event(self, button: ctk.CTkButton):
        """ Is used in quizz """
        grades = [0, 0.2, 0.5, 1]
        for i in range(4):  # Hardcoded `grades` length
            if self.subcounter == grades[i]:
                self.subcounter = grades[i + 1]
                break
        button.configure(state='disabled', fg_color='red')

    def set_sidebar(self, state: str, *exception) -> None:
        sidebar = (self.themes_combobox, self.tests_combobox, self.start_test_button, self.edit_test_button,
                   self.add_words_button, self.delete_test_button, self.create_button)
        for item in sidebar:
            if item not in exception:
                item.configure(state=state)

    def theme_option_menu_event(self, new_theme):
        self.selected_theme = new_theme
        self.update_test_files()
        self.update_sidebar()
        self.show_test_preview()

    def test_option_menu_event(self, new_test):
        self.selected_test = new_test
        validate_testfile(rf'{OPER_FOLDER}{self.selected_theme}\{self.selected_test}.test')
        self.show_test_preview()

    def update_theme_folders(self) -> None:
        self.themes = []
        for folder in listdir(OPER_FOLDER):
            self.themes.append(folder)
        # if selected theme is None or doesn't exits anymore, and there is one found -> select it
        if self.selected_theme not in self.themes and self.themes:
            self.selected_theme = self.themes[0]
        else:
            self.selected_theme = None

    def update_test_files(self) -> None:
        folder = f"{OPER_FOLDER}{self.selected_theme}"
        self.tests = []
        for filename in listdir(folder):
            if filename.endswith(".test"):
                test_name = filename[:-5:]  # removing file's extension from a name
                self.tests.append(test_name)
        # if selected test is None or doesn't exits anymore, and there is one found -> select it
        if self.tests:
            if self.selected_test not in self.tests:
                self.selected_test = self.tests[0]
        else:
            self.selected_test = None

def mix(array) -> list:
    """Returns a shuffled list without changing the original"""
    temp = array[:]
    shuffle(temp)
    return temp


def check_valid_input(*entries: ctk.CTkEntry, include=None, exclude=()) -> bool:
    """Makes an entry red if invalid, else default grey
    :param exclude: input is valid if it doesn't contain values from here
    :param include: input is valid if it only contains values from here
    :returns: True if **all** inputs are valid, else False
    """
    is_valid = True
    for entry in entries:
        text = entry.get().strip()
        if text and text == ''.join(takewhile(lambda x: x not in exclude and (include is None or x in include), text)):
            entry.configure(fg_color="#353638", border_color='#555560')
        else:
            entry.configure(fg_color="darkred", border_color='red')
            entry.focus_set()
            is_valid = False
    return is_valid


def validate_testfile(test_path: str) -> None:
    """Removes empty lines and trailing spaces from file. Sorts the words alphabetically"""
    text = get_text_from_file(test_path)
    for i in range(len(text) - 1, -1, -1):
        word_pair = text[i].split(' - ')
        if len(word_pair) != 2:
            text.pop(i)
            continue
        word_pair = [j.strip().capitalize() for j in word_pair]
        text[i] = f"{word_pair[0]} - {word_pair[1]}\n"

    with open(test_path, 'w', encoding=ENCODING) as file:
        for line in sorted(text):
            file.write(line)


def get_text_from_file(file_path: str) -> list[str]:
    text = open(file_path, 'r', encoding=ENCODING).readlines()
    return text


def check_oper_folder():
    makedirs(OPER_FOLDER, exist_ok=True)  # makes a folder if there wasn't already one


if __name__ == "__main__":
    app = App()
    check_oper_folder()
    app.update_sidebar()
    app.mainloop()

# TODO:
#   1. Installation + Deletion
#   2. Operating from user's folder
#   3. Automatically generate new test when 30 words are reached (Check if newly created test already exists)
#   4. Make settings support (language change, theme, and disabling third paragraph)
#   5. Make automatic translate suggestions (Based on selected language)
#   6. Multi languge learning support
#   7. Make a license if paragraph 1 and 2 didn't help with the app being considered a virus
#   8. Add voice assistance
#   9. Add sentence examples


