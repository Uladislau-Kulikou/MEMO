from os import remove, rmdir

import customtkinter as ctk
from globals import OPER_FOLDER

"""A frame where we can delete a new Theme/Test"""


class TestDeletion(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color="#191919")
        self.root = root
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        self.confirmation_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=34, weight="bold"),
                                               wraplength=620, justify=ctk.CENTER)
        self.confirmation_label.grid(row=1, columnspan=2, pady=(0, 100))

        self.decline_button = ctk.CTkButton(self, text='No', command=self.decline_deletion_event,
                                            height=50, font=ctk.CTkFont(size=20), width=100)
        self.decline_button.grid(row=2, column=0, padx=(0, 50), sticky='e')

        self.accept_button = ctk.CTkButton(self, text='Yes', command=self.accept_deletion_event,
                                           height=50, font=ctk.CTkFont(size=20), width=100, fg_color="red",
                                           hover_color="darkred")
        self.accept_button.grid(row=2, column=1, padx=(50, 0), sticky='w')

    def delete_test_button_event(self):
        self.root.sidebar.set('disabled')
        self.root.update_theme_folders()
        self.root.update_test_files()
        if self.root.tests:
            text = f'Are you sure you want to delete test "{self.root.selected_test}" from "{self.root.selected_theme}"?'
        else:
            text = f'Are you sure you want to delete theme "{self.root.selected_theme}"?'
        self.confirmation_label.configure(text=text)
        self.root.set_current_frame(self)

    def decline_deletion_event(self):
        self.root.sidebar.set('normal')
        self.root.test_preview_frame.show()

    def accept_deletion_event(self):
        self.root.sidebar.set('normal')
        if self.root.tests:
            remove(rf'{OPER_FOLDER}{self.root.selected_theme}\{self.root.selected_test}.test')  # Deletes file
        else:
            rmdir(rf'{OPER_FOLDER}{self.root.selected_theme}')
        self.root.update_theme_folders()
        self.root.update_test_files()
        self.root.sidebar.refresh()
        self.root.test_preview_frame.show()

