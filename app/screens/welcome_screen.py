import tkinter as tk

class WelcomeScreen(tk.Frame):
    def __init__(self, master, switch_screen_callback=None):
        super().__init__(master)
        self.master = master
        self.switch_screen_callback = switch_screen_callback

        # Make window full screen
        self.master.state("zoomed")
        self.master.configure(bg="#B22222")  # Background dark red

        self.create_widgets()

    def create_widgets(self):
        # 1️⃣ Big outer rectangle (touches window edges, dark red)
        self.big_frame = tk.Frame(
            self,
            bg="#8B0000",  # Dark red
            bd=0
        )
        self.big_frame.pack(fill="both", expand=True)

        # 2️⃣ Middle rectangle (white, centered)
        self.outer_frame = tk.Frame(
            self.big_frame,
            bg="#FFFFFF",
            bd=0
        )
        self.outer_frame.place(relx=0.5, rely=0.5, anchor="center",
                               relwidth=0.6, relheight=0.5)

        # 3️⃣ Inner rectangle (dark gray) inside middle rectangle
        self.inner_frame = tk.Frame(
            self.outer_frame,
            bg="#3a3a3a",
            bd=0
        )
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center",
                               relwidth=0.95, relheight=0.9)

        # Multi-line welcome text
        self.welcome_label = tk.Label(
            self.inner_frame,
            text="CAMPUS SCHEDULE\nMANAGEMENT SYSTEM",
            font=("Helvetica", 36, "bold"),
            fg="white",
            bg="#3a3a3a",
            justify="center"
        )
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

        # Next button (bottom-right) inside big_frame
        self.next_button = tk.Button(
            self.big_frame,
            text="Next →",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="black",
            command=self.go_to_next
        )
        self.next_button.place(relx=0.98, rely=0.95, anchor="se")  # stays at bottom-right

    def go_to_next(self):
        if self.switch_screen_callback:
            self.switch_screen_callback("login")
