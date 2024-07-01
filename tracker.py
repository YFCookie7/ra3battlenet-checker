import customtkinter as ctk


class Tracker(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.isTracking = False
        self.after(1000, self.start_tracking)

    def toogle_tracking(self):
        self.isTracking = not self.isTracking

    def start_tracking(self):
        if self.isTracking:
            print("qwe")
        self.after(1000, self.start_tracking)
