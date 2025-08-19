import customtkinter as ctk

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