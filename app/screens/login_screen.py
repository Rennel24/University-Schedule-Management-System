import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import mysql.connector


def connect_db():
    """Helper function to connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
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
    # ========================= BACKGROUND IMAGE =========================
        try:
            bg_image = Image.open(r"E:\UniversityScheduleSystem\assets\background.png")

            # Resize to screen size
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            opacity_value = 0.35
            # Convert image to RGBA to support alpha fade
            bg_image = bg_image.convert("RGBA")
            alpha = bg_image.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity_value)
            bg_image.putalpha(alpha)

            # Create final PhotoImage
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            # Background label
            self.bg_label = tk.Label(self, image=self.bg_photo, bg="#890d0d")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
         
        except:
            self.configure(bg="#f0f0f0")  # fallback solid color

        # ========================= HEADER =========================
        self.header_frame = tk.Frame(self, bg="#be0b0b", height=100)
        self.header_frame.pack(fill="x", side="top")

        self.header_frame.columnconfigure(0, weight=1)
        self.header_frame.columnconfigure(1, weight=10)
        self.header_frame.columnconfigure(2, weight=1)

        # --- LEFT LOGO ---
        try:
            img = Image.open(r"E:\UniversityScheduleSystem\assets\cics_background.png")
            img = img.resize((98, 97), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(img)
            self.logo = tk.Label(self.header_frame, image=self.logo_image, bg="#be0b0b")
        except:
            self.logo = tk.Label(
                self.header_frame,
                text="🏫",
                bg="#890d0d",
                fg="white",
                font=("Segoe UI", 32, "bold")
            )
        self.logo.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        # --- CENTER TITLE ---
        self.title_label = tk.Label(
            self.header_frame,
            text="Campus Schedule Management System",
            bg="#be0b0b",
            fg="white",
            font=("Georgia", 33, "bold"),
            anchor="center",
            justify="center"
        )
        self.title_label.grid(row=0, column=1, sticky="nsew", padx=10)

        # ========================= LOGIN CARD =========================
        self.card_frame = tk.Frame(
            self,
            bg="white",
            width=480,
            height=330,
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.card_frame.place(relx=0.5, rely=0.55, anchor="center")
        self.card_frame.pack_propagate(False)

        tk.Label(
            self.card_frame,
            text="ADMIN LOGIN",
            bg="white",
            fg="black",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(20, 10))

        # ---------- USERNAME ----------
        tk.Label(
            self.card_frame,
            text="USERNAME",
            bg="white",
            fg="black",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=50)

        self.username_entry = tk.Entry(
            self.card_frame,
            bg="#e6e6e6",
            fg="black",
            font=("Segoe UI", 12),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#bbbbbb",
            width=28
        )
        self.username_entry.pack(pady=(5, 15), ipady=5, padx=50, fill="x")

        # ---------- PASSWORD ----------
        tk.Label(
            self.card_frame,
            text="PASSWORD",
            bg="white",
            fg="black",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=50)

        self.password_entry = tk.Entry(
            self.card_frame,
            bg="#e6e6e6",
            fg="black",
            font=("Segoe UI", 12),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#bbbbbb",
            width=28,
            show="*"
        )
        self.password_entry.pack(pady=(5, 20), ipady=5, padx=50, fill="x")

        # ---------- LOGIN BUTTON ----------
        self.login_button = tk.Button(
            self.card_frame,
            text="LOGIN",
            bg="#890d0d",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=12,
            height=1,
            relief="flat",
            cursor="hand2",
            command=self.login
        )
        self.login_button.pack(pady=(5, 5))

        # Enter key binds to login
        self.master.bind("<Return>", lambda e: self.login())

        # ========================= BACK BUTTON =========================
        self.back_button = tk.Button(
            self,
            text="Back",
            bg="#d60000",                
            fg="#FFFFFF",
            font=("Segoe UI", 12, "bold"), 
            relief="flat",
            cursor="hand2",
            activebackground="#bfbfbf",    
            activeforeground="black",
            bd=0,                        
            highlightthickness=0,
            padx=15,                      
            pady=8,                        
            command=self.go_back
        )
        self.back_button.place(x=20, rely=1, y=-20, anchor="sw")


    # ========================= NAVIGATION =========================
    def go_back(self):
        if self.switch_screen_callback:
            self.switch_screen_callback("welcome")

    # ========================= LOGIN FUNCTION =========================
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
