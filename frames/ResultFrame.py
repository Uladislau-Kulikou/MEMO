import customtkinter as ctk

"""Shows user the result (score) of his  test (any kind)"""

class ResultFrame(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root, corner_radius=0, fg_color="#191919")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=34, weight="bold"), corner_radius=0)
        self.result_label.grid(row=0, column=0, sticky="nsew")