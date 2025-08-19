import customtkinter as ctk

"""This frame shows us 2 options, whethere we want to create a theme (category of tests) or a test"""

class CreateFile(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color="#191919")
        self.root = root
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_theme_button = ctk.CTkButton(self, command=root.test_creation_frame.create_theme_button_event,
                                                 text='New theme', height=60, font=ctk.CTkFont(size=30))
        self.create_theme_button.grid(row=1, column=0, sticky='nse', padx=(50, 50))

        self.create_test_button = ctk.CTkButton(self, command=root.test_creation_frame.create_test_button_event,
                                                text='New test', height=60, font=ctk.CTkFont(size=30))
        self.create_test_button.grid(row=1, column=1, sticky='nsw', padx=(50, 50))

    def create_button_event(self):
        if not self.root.selected_theme:
            # If not theme was found, we redirect the user immediately to theme creation frame
            self.root.test_creation_frame.create_theme_button_event()
            return
        self.root.set_current_frame(self)