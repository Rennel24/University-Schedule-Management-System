import tkinter as tk
from tkinter import PhotoImage, messagebox
import mysql.connector

def connect_db():
    """Helper function to connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # update if you set MySQL password
        database="university_schedule_db"
    )

class LoginScreen(tk.Frame):
    def __init__(self, master, switch_screen_callback=None):
        super().__init__(master)
        self.master = master
        self.switch_screen_callback = switch_screen_callback

        self.master.configure(bg="#f8f8f8")
        self.master.state("zoomed")
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_frame = tk.Frame(self, bg="#890d0d", height=100)
        self.header_frame.pack(fill="x", side="top")

        try:
            self.logo_image = tk.PhotoImage(file=r"E:\UniversityScheduleSystem\assets\icons\BatStateU-NEU-Logo.png")
            self.logo = tk.Label(self.header_frame, image=self.logo_image, bg="#890d0d")
            self.logo.pack(side="left", padx=20, pady=20)
        except Exception as e:
            print("Logo not found:", e)
            self.logo = tk.Label(self.header_frame, text="🏫", bg="#890d0d", fg="white", font=("Arial", 38))
            self.logo.pack(side="left", padx=20, pady=20)

        self.title_label = tk.Label(
            self.header_frame,
            text="Alangilan Campus Academic Schedule System",
            bg="#890d0d",
            fg="white",
            font=("Times New Roman", 38, "bold")
        )
        self.title_label.pack(side="left", pady=20, padx=10)

        # Login Card
        self.card_frame = tk.Frame(self, bg="white", width=500, height=350,
                                   highlightthickness=1, highlightbackground="#cccccc")
        self.card_frame.place(relx=0.5, rely=0.55, anchor="center")
        self.card_frame.pack_propagate(False)

        tk.Label(self.card_frame, text="ADMIN", bg="white", fg="black",
                 font=("Arial", 26, "bold")).pack(pady=(25, 20))

        tk.Label(self.card_frame, text="USERNAME:", bg="white", fg="black",
                 font=("Arial", 15, "bold")).pack(anchor="w", padx=80)
        self.username_entry = tk.Entry(self.card_frame, bg="#868686", fg="white",
                                       font=("Arial", 14), relief="flat")
        self.username_entry.pack(pady=(5, 20), ipady=5, padx=80, fill="x")

        tk.Label(self.card_frame, text="PASSWORD:", bg="white", fg="black",
                 font=("Arial", 15, "bold")).pack(anchor="w", padx=80)
        self.password_entry = tk.Entry(self.card_frame, bg="#868686", fg="white",
                                       font=("Arial", 14), relief="flat", show="*")
        self.password_entry.pack(pady=(5, 30), ipady=5, padx=80, fill="x")

        self.login_button = tk.Button(self.card_frame, text="LOGIN",
                                      bg="#890d0d", fg="white",
                                      font=("Arial", 20, "bold"), relief="flat",
                                      cursor="hand2", command=self.login)
        self.login_button.pack(pady=(5, 15))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT admin_id, admin_name, college_id
                FROM admins
                WHERE username = %s AND password = %s
            """
            cursor.execute(query, (username, password))
            admin_data = cursor.fetchone()

            if admin_data:
                if admin_data['college_id'] != 4:
                    messagebox.showerror("Access Denied", "Only CICS admins can log in here.")
                else:
                    messagebox.showinfo("Login Successful", f"Welcome, {admin_data['admin_name']}!")
                    if self.switch_screen_callback:
                        self.switch_screen_callback("dashboard", admin_data)
            else:
                messagebox.showerror("Invalid Login", "Incorrect username or password.")

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Unable to connect to database:\n{err}")
