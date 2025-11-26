import tkinter as tk
from datetime import datetime
from tkinter import PhotoImage
import mysql.connector

def connect_db():
    """Helper function to connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # set your MySQL password
        database="university_schedule_db"
    )

class DashboardScreen(tk.Frame):
    def __init__(self, master, switch_screen_callback=None, admin_data=None):
        super().__init__(master)
        self.master = master
        self.switch_screen_callback = switch_screen_callback
        self.admin_data = admin_data

        self.configure(bg="#f8f8f8")
        self.create_widgets()
        self.update_time()
        self.load_dashboard_data()  # load initial data

    def create_widgets(self):
        # ---------------- TOP BAR 1 ----------------
        self.top_frame = tk.Frame(self, bg="#890d0d", height=80)
        self.top_frame.pack(fill="x", side="top")

        # Logo image
        try:
            self.logo_image = PhotoImage(file=r"assets/logo_top.png")
            tk.Label(self.top_frame, image=self.logo_image, bg="#890d0d").pack(side="left", padx=20, pady=10)
        except:
            tk.Label(self.top_frame, text="🏫", bg="#890d0d", fg="white", font=("Arial", 36)).pack(side="left", padx=20, pady=10)

        # System title
        tk.Label(self.top_frame, text="Alangilan Campus Academic Schedule System",
                 bg="#890d0d", fg="white", font=("Times New Roman", 28, "bold")).pack(side="left", padx=10)

        # ---------------- TOP BAR 2 ----------------
        self.top_bar2 = tk.Frame(self, bg="#b22222", height=40)
        self.top_bar2.pack(fill="x", side="top")

        admin_name = self.admin_data['admin_name'] if self.admin_data else "Admin"

        # Center Welcome Label
        self.welcome_label = tk.Label(self.top_bar2, text=f"Welcome {admin_name}",
                                      bg="#b22222", fg="white", font=("Arial", 14, "bold"))
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

        # Date/Time on the right
        self.datetime_label = tk.Label(self.top_bar2, bg="#b22222", fg="white", font=("Arial", 14))
        self.datetime_label.pack(side="right", padx=20)

        # ---------------- LEFT SIDEBAR ----------------
        self.sidebar_frame = tk.Frame(self, bg="#3a3a3a", width=180)
        self.sidebar_frame.pack(side="left", fill="y")

        tk.Label(self.sidebar_frame, text="MENU", bg="#3a3a3a", fg="white",
                 font=("Arial", 16, "bold")).pack(pady=(20,10))

        # Sidebar logo
        try:
            self.sidebar_logo = PhotoImage(file=r"assets/logo_sidebar.png")
            tk.Label(self.sidebar_frame, image=self.sidebar_logo, bg="#3a3a3a").pack(pady=10)
        except:
            tk.Label(self.sidebar_frame, text="🏫", bg="#3a3a3a", fg="white", font=("Arial", 36)).pack(pady=10)

        # Menu buttons
        menu_items = ["DASHBOARD", "SCHEDULE"]
        for btn_text in menu_items:
            b = tk.Button(self.sidebar_frame, text=btn_text, bg="#3a3a3a", fg="white",
                          font=("Arial", 14, "bold"), relief="flat", cursor="hand2",
                          command=lambda t=btn_text: self.menu_action(t))
            b.pack(fill="x", pady=5, padx=10)

        # ---------------- MAIN CONTENT ----------------
        self.cards_frame = tk.Frame(self, bg="#f8f8f8")
        self.cards_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Prepare placeholders for the card widgets to update values
        self.card_widgets = []

        totals_template = [
            ("TOTAL COLLEGES", r"assets/icons/college.png"),
            ("TOTAL PROGRAMS", r"assets/icons/program.png"),
            ("TOTAL PROFESSORS", r"assets/icons/professor.png"),
            ("TOTAL SECTIONS", r"assets/icons/section.png"),
            ("TOTAL COURSES", r"assets/icons/course.png"),
            ("TOTAL SCHEDULES", r"assets/icons/schedule.png"),
        ]

        rows, cols = 2, 3
        index = 0
        for r in range(rows):
            for c in range(cols):
                if index >= len(totals_template):
                    break
                title, icon_path = totals_template[index]

                card = tk.Frame(self.cards_frame, bg="#890d0d", width=200, height=120)
                card.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
                card.grid_propagate(False)

                # Icon
                try:
                    icon_img = PhotoImage(file=icon_path)
                    tk.Label(card, image=icon_img, bg="#890d0d").pack(pady=(10,0))
                    card.icon_img = icon_img
                except:
                    tk.Label(card, text="📌", bg="#890d0d", fg="white", font=("Arial", 20)).pack(pady=(10,0))

                # Title
                title_label = tk.Label(card, text=title, bg="#890d0d", fg="white", font=("Arial", 12, "bold"))
                title_label.pack()
                # Value (dynamic)
                value_label = tk.Label(card, text="0", bg="#890d0d", fg="white", font=("Arial", 20, "bold"))
                value_label.pack()

                self.card_widgets.append((title, value_label))
                index += 1

        for i in range(cols):
            self.cards_frame.columnconfigure(i, weight=1)
        for i in range(rows):
            self.cards_frame.rowconfigure(i, weight=1)

    def menu_action(self, menu_name):
        if menu_name == "DASHBOARD":
            self.load_dashboard_data()  # refresh dashboard
        elif menu_name == "SCHEDULE" and self.switch_screen_callback:
            self.switch_screen_callback("schedule", self.admin_data)
        else:
            print(f"{menu_name} clicked")


    def load_dashboard_data(self):
        """Fetch latest counts from the database and update cards."""
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Example queries, replace with your actual table structure
            cursor.execute("SELECT COUNT(*) FROM colleges")
            total_colleges = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM programs")
            total_programs = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM professors")
            total_professors = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM sections")
            total_sections = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM courses")
            total_courses = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM schedules")
            total_schedules = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            # Update card values
            data_map = {
                "TOTAL COLLEGES": total_colleges,
                "TOTAL PROGRAMS": total_programs,
                "TOTAL PROFESSORS": total_professors,
                "TOTAL SECTIONS": total_sections,
                "TOTAL COURSES": total_courses,
                "TOTAL SCHEDULES": total_schedules
            }

            for title, value_label in self.card_widgets:
                value_label.config(text=data_map.get(title, 0))

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def update_time(self):
        now = datetime.now()
        self.datetime_label.config(text=now.strftime("%m/%d/%Y   %I:%M:%S %p"))
        self.after(1000, self.update_time)
