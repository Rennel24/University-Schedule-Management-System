import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from datetime import datetime
import mysql.connector


def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Update with your password
        database="university_schedule_db"
    )


class ScheduleScreen(tk.Frame):
    def __init__(self, master, switch_screen_callback=None, admin_data=None):
        super().__init__(master)
        self.master = master
        self.switch_screen_callback = switch_screen_callback
        self.admin_data = admin_data

        # UI state
        self.selected_schedule_id = None  # used for update/delete

        # Time options
        self.time_start_values = [
            "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM",
            "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM",
            "05:00 PM", "06:00 PM"
        ]
        self.time_end_values = [
            "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
            "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM",
            "06:00 PM", "07:00 PM", "08:00 PM"
        ]

        self.configure(bg="#f8f8f8")

        # Build UI
        self.create_top_bars()
        self.create_sidebar()
        self.create_search_filter_bar()
        self.create_table_section()
        self.create_input_fields()
        self.create_action_buttons()

        # Start time updater and initial loads
        self.update_time()
        self.load_dropdowns_static()
        self.load_schedule_data()

    # ---------------- TOP BARS ----------------
    def create_top_bars(self):
        self.top_frame = tk.Frame(self, bg="#890d0d", height=80)
        self.top_frame.pack(fill="x", side="top")

        try:
            self.logo_image = PhotoImage(file=r"assets/logo_top.png")
            tk.Label(self.top_frame, image=self.logo_image, bg="#890d0d").pack(side="left", padx=20, pady=10)
        except:
            tk.Label(self.top_frame, text="🏫", bg="#890d0d", fg="white", font=("Arial", 36)).pack(side="left", padx=20, pady=10)

        tk.Label(self.top_frame, text="Alangilan Campus Academic Schedule System",
                 bg="#890d0d", fg="white", font=("Times New Roman", 28, "bold")).pack(side="left", padx=10)

        logout_btn = tk.Button(self.top_frame, text="Logout", bg="#ff4c4c", fg="white",
                               font=("Arial", 12, "bold"), cursor="hand2", command=self.logout)
        logout_btn.pack(side="right", padx=20, pady=20)

        self.top_bar2 = tk.Frame(self, bg="#b22222", height=40)
        self.top_bar2.pack(fill="x", side="top")
        tk.Label(self.top_bar2, text="Schedule Management",
                 bg="#b22222", fg="white", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        self.datetime_label = tk.Label(self.top_bar2, bg="#b22222", fg="white", font=("Arial", 14))
        self.datetime_label.pack(side="right", padx=20)

    # ---------------- SIDEBAR ----------------
    def create_sidebar(self):
        self.sidebar_frame = tk.Frame(self, bg="#3a3a3a", width=180)
        self.sidebar_frame.pack(side="left", fill="y")

        tk.Label(self.sidebar_frame, text="MENU", bg="#3a3a3a", fg="white",
                 font=("Arial", 16, "bold")).pack(pady=(20, 10))

        try:
            self.sidebar_logo = PhotoImage(file=r"assets/logo_sidebar.png")
            tk.Label(self.sidebar_frame, image=self.sidebar_logo, bg="#3a3a3a").pack(pady=10)
        except:
            tk.Label(self.sidebar_frame, text="🏫", bg="#3a3a3a", fg="white", font=("Arial", 36)).pack(pady=10)

        menu_items = ["DASHBOARD", "SCHEDULE"]
        for btn_text in menu_items:
            b = tk.Button(self.sidebar_frame, text=btn_text, bg="#3a3a3a", fg="white",
                          font=("Arial", 14, "bold"), relief="flat", cursor="hand2",
                          command=lambda t=btn_text: self.menu_action(t))
            b.pack(fill="x", pady=5, padx=10)

    # ---------------- SEARCH/FILTER BAR ----------------
    def create_search_filter_bar(self):
        self.search_frame = tk.Frame(self, bg="#f0f0f0", height=40)
        self.search_frame.pack(fill="x", padx=20, pady=(10, 0))

        tk.Label(self.search_frame, text="Filter by Day:", bg="#f0f0f0", font=("Arial", 12)).pack(side="left", padx=(10, 5))
        self.filter_option = ttk.Combobox(self.search_frame, values=["All", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], state="readonly", width=10)
        self.filter_option.pack(side="left", padx=(0, 10))
        self.filter_option.current(0)

        tk.Button(self.search_frame, text="Show All", bg="#890d0d", fg="white",
                  font=("Arial", 12, "bold"), cursor="hand2", command=self.load_schedule_data).pack(side="left", padx=(10, 0))

        tk.Button(self.search_frame, text="Filter", bg="#4a90e2", fg="white",
                  font=("Arial", 12, "bold"), cursor="hand2", command=self.apply_filter).pack(side="left", padx=(6, 0))

    # ---------------- TABLE ----------------
    def create_table_section(self):
        self.table_frame = tk.Frame(self, bg="#f8f8f8")
        self.table_frame.pack(padx=20, pady=(10, 0), fill="both", expand=True)

        columns = ["schedule_id", "section", "program", "course_code", "course_name",
                   "professor", "day", "start_time", "end_time", "room"]
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col.title().replace("_", " "))
            # give schedule_id narrower column
            width = 80 if col == "schedule_id" else 120
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # vertical scrollbar
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')

    # ---------------- INPUT FIELDS ----------------
    def create_input_fields(self):
        self.input_frame = tk.Frame(self, bg="#f8f8f8")
        self.input_frame.pack(padx=20, pady=(10, 0), fill="x")

        self.entries = {}

        # columns layout
        col1 = tk.Frame(self.input_frame, bg="#f8f8f8")
        col2 = tk.Frame(self.input_frame, bg="#f8f8f8")
        col3 = tk.Frame(self.input_frame, bg="#f8f8f8")
        col1.pack(side="left", padx=10, fill="y")
        col2.pack(side="left", padx=10, fill="y")
        col3.pack(side="left", padx=10, fill="y")

        # labels + comboboxes (initially empty lists, we'll populate from DB)
        fields_col1 = ["Section", "Program", "Course Code"]
        fields_col2 = ["Course Name", "Day", "Time Start", "Time End"]
        fields_col3 = ["Professor", "Room"]

        for f in fields_col1:
            tk.Label(col1, text=f + ":", bg="#f8f8f8", font=("Arial", 12)).pack(anchor="w")
            cb = ttk.Combobox(col1, values=[], state="readonly")
            cb.pack(pady=5, fill="x")
            self.entries[f] = cb

        for f in fields_col2:
            tk.Label(col2, text=f + ":", bg="#f8f8f8", font=("Arial", 12)).pack(anchor="w")
            if f == "Time Start":
                cb = ttk.Combobox(col2, values=self.time_start_values, state="readonly")
                cb.current(0)
            elif f == "Time End":
                cb = ttk.Combobox(col2, values=self.time_end_values, state="readonly")
                cb.current(0)
            else:
                cb = ttk.Combobox(col2, values=[], state="readonly")
            cb.pack(pady=5, fill="x")
            self.entries[f] = cb

        # bind start -> update end options
        self.time_start_combo = self.entries["Time Start"]
        self.time_end_combo = self.entries["Time End"]
        self.time_start_combo.bind("<<ComboboxSelected>>", self.update_time_end_options)

        for f in fields_col3:
            tk.Label(col3, text=f + ":", bg="#f8f8f8", font=("Arial", 12)).pack(anchor="w")
            cb = ttk.Combobox(col3, values=[], state="readonly")
            cb.pack(pady=5, fill="x")
            self.entries[f] = cb

        # quick reference
        self.room_entry = self.entries["Room"]

    # ---------------- ACTION BUTTONS ----------------
    def create_action_buttons(self):
        self.button_frame = tk.Frame(self, bg="#f8f8f8")
        self.button_frame.pack(pady=10)

        btns = {
            "Save": self.save_schedule,
            "Update": self.update_schedule,
            "Clear": self.clear_fields,
            "Delete": self.delete_schedule
        }

        for text, cmd in btns.items():
            tk.Button(
                self.button_frame,
                text=text,
                bg="#890d0d",
                fg="white",
                font=("Arial", 12, "bold"),
                width=10,
                cursor="hand2",
                command=cmd
            ).pack(side="left", padx=10)

    # ---------------- MENU ACTIONS ----------------
    def menu_action(self, menu_name):
        if menu_name == "DASHBOARD" and self.switch_screen_callback:
            self.switch_screen_callback("dashboard")
        elif menu_name == "SCHEDULE":
            self.load_schedule_data()
        else:
            messagebox.showinfo("Info", f"{menu_name} clicked")

    # ---------------- LOAD DROPDOWNS FROM DB ----------------
    def load_dropdowns_static(self):
        """Populate comboboxes with static values."""
        
        programs = ["BSIT", "BSCS", "BSECE"]
        sections = ["BSIT 2101", "BSIT 2102", "BSCS 2201"]
        course_codes = ["IT 211", "CS 121", "MATH101"]
        course_names = ["Data Structures", "Programming 1", "Calculus 1"]
        professors = ["Joana Reyes", "De Castro Mariel", "Juan Dela Cruz"]
        rooms = ["Room 201", "Room 202", "Lab 1"]
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        # Populate comboboxes
        self.entries["Program"]["values"] = programs
        self.entries["Section"]["values"] = sections
        self.entries["Course Code"]["values"] = course_codes
        self.entries["Course Name"]["values"] = course_names
        self.entries["Professor"]["values"] = professors
        self.entries["Room"]["values"] = rooms
        self.entries["Day"]["values"] = days

        # Set defaults if not set
        for k, cb in self.entries.items():
            if isinstance(cb, ttk.Combobox):
                if not cb.get() and cb["values"]:
                    cb.current(0)


    # ---------------- LOAD SCHEDULE DATA ----------------
    def load_schedule_data(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        selected_day = self.filter_option.get().strip()

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    sched.schedule_id,
                    sec.section_name AS Section,
                    prog.program_name AS Program,
                    c.course_code AS `Course Code`,
                    c.course_name AS `Course Name`,
                    CONCAT(prof.first_name, ' ', prof.last_name) AS Professor,
                    d.day_name AS Day,
                    TIME_FORMAT(sched.start_time, '%h:%i %p') AS `Time Start`,
                    TIME_FORMAT(sched.end_time, '%h:%i %p') AS `Time End`,
                    r.room_name AS Room
                FROM schedules sched
                LEFT JOIN sections sec ON sched.section_id = sec.section_id
                LEFT JOIN programs prog ON sec.program_id = prog.program_id
                LEFT JOIN courses c ON sched.course_id = c.course_id
                LEFT JOIN professors prof ON sched.professor_id = prof.professor_id
                LEFT JOIN rooms r ON sched.room_id = r.room_id
                LEFT JOIN days d ON sched.day_id = d.day_id
            """

            params = ()
            if selected_day and selected_day.lower() != "all":
                query += " WHERE LOWER(d.day_name) = LOWER(%s)"
                params = (selected_day,)

            query += " ORDER BY sched.schedule_id"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            for r in rows:
                self.tree.insert("", "end", values=(
                    r.get('schedule_id'),
                    r.get('Section'),
                    r.get('Program'),
                    r.get('Course Code'),
                    r.get('Course Name'),
                    r.get('Professor'),
                    r.get('Day'),
                    r.get('Time Start'),
                    r.get('Time End'),
                    r.get('Room'),
                ))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            messagebox.showerror("Database Error", f"Failed to load schedules:\n{err}")


    # ---------------- APPLY FILTER ----------------
    def apply_filter(self):
        self.load_schedule_data()

    # ---------------- TREE SELECT ----------------
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        vals = item.get("values", [])
        if not vals:
            return
        # fill input fields - assuming order matches load_schedule_data
        self.selected_schedule_id = vals[0]
        # Set comboboxes safely (if value not in values, add it temporarily)
        mapping = {
            "Section": vals[1],
            "Program": vals[2],
            "Course Code": vals[3],
            "Course Name": vals[4],
            "Professor": vals[5],
            "Day": vals[6],
            "Time Start": vals[7],
            "Time End": vals[8],
            "Room": vals[9],
        }
        for key, val in mapping.items():
            cb = self.entries.get(key)
            if isinstance(cb, ttk.Combobox):
                # Only add the value if it is non-empty and not already in values
                if val and val not in cb["values"]:
                    new_values = [val] + list(cb["values"])
                    cb["values"] = new_values
                try:
                    cb.set(val)
                except Exception:
                    pass

    # ---------------- CLEAR FIELDS ----------------
    def clear_fields(self):
        self.selected_schedule_id = None
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                if entry["values"]:
                    entry.current(0)
                else:
                    entry.set("")
            else:
                try:
                    entry.delete(0, tk.END)
                except Exception:
                    pass

    # ---------------- TIME HELPERS ----------------
    def update_time_end_options(self, event):
        start = self.time_start_combo.get()
        if not start:
            return
        valid_end_times = [t for t in self.time_end_values if self.time_to_minutes(t) > self.time_to_minutes(start)]
        self.time_end_combo.config(values=valid_end_times)
        if valid_end_times:
            # if current end not valid, set to first valid
            if self.time_end_combo.get() not in valid_end_times:
                self.time_end_combo.set(valid_end_times[0])

    def time_to_minutes(self, t):
        dt = datetime.strptime(t, "%I:%M %p")
        return dt.hour * 60 + dt.minute

    def validate_time(self):
        time_start = self.entries["Time Start"].get()
        time_end = self.entries["Time End"].get()
        if not time_start or not time_end:
            messagebox.showerror("Invalid Time", "Please select both Time Start and Time End.")
            return False
        t_start = datetime.strptime(time_start, "%I:%M %p")
        t_end = datetime.strptime(time_end, "%I:%M %p")
        if t_end <= t_start:
            messagebox.showerror("Invalid Time", "Time End must be later than Time Start.")
            return False
        return True

    # ---------------- GET OR CREATE HELPERS ----------------
    # These helpers use the provided cursor and do NOT commit individually.
    # Caller controls commit/rollback.

    def get_or_create_program(self, program_name, cursor):
        cursor.execute("SELECT program_id FROM programs WHERE LOWER(program_name)=LOWER(%s)", (program_name,))
        row = cursor.fetchone()
        if row:
            return row[0], False
        cursor.execute("INSERT INTO programs (program_name) VALUES (%s)", (program_name,))
        return cursor.lastrowid, True

    def get_or_create_section(self, section_name, program_name, cursor):
        program_id, _ = self.get_or_create_program(program_name, cursor)
        cursor.execute("SELECT section_id FROM sections WHERE LOWER(section_name)=LOWER(%s) AND program_id=%s",
                       (section_name, program_id))
        row = cursor.fetchone()
        if row:
            return row[0], False
        cursor.execute("INSERT INTO sections (section_name, program_id) VALUES (%s,%s)", (section_name, program_id))
        return cursor.lastrowid, True

    def get_or_create_course(self, course_code, course_name, program_name, cursor):
        program_id, _ = self.get_or_create_program(program_name, cursor)
        # Check by code AND name
        cursor.execute("""
            SELECT course_id FROM courses 
            WHERE LOWER(course_code)=LOWER(%s) AND program_id=%s
        """, (course_code, program_id))
        row = cursor.fetchone()
        if row:
            # Optional: update course name if different
            cursor.execute("""
                UPDATE courses SET course_name=%s WHERE course_id=%s
            """, (course_name, row[0]))
            return row[0], False
        cursor.execute("""
            INSERT INTO courses (course_code, course_name, program_id) 
            VALUES (%s, %s, %s)
        """, (course_code, course_name, program_id))
        return cursor.lastrowid, True


    def get_or_create_professor(self, prof_name, cursor):
        name = (prof_name or "").strip()
        if not name:
            return None, False
        parts = name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
        cursor.execute(
            "SELECT professor_id FROM professors WHERE LOWER(first_name)=LOWER(%s) AND LOWER(last_name)=LOWER(%s)",
            (first_name, last_name)
        )
        row = cursor.fetchone()
        if row:
            return row[0], False
        cursor.execute("INSERT INTO professors (first_name, last_name) VALUES (%s,%s)", (first_name, last_name))
        return cursor.lastrowid, True

    def get_or_create_room(self, room_name, cursor):
        cursor.execute("SELECT room_id FROM rooms WHERE LOWER(room_name)=LOWER(%s)", (room_name,))
        row = cursor.fetchone()
        if row:
            return row[0], False
        cursor.execute("INSERT INTO rooms (room_name) VALUES (%s)", (room_name,))
        return cursor.lastrowid, True

    def get_or_create_day(self, day_name, cursor):
        cursor.execute("SELECT day_id FROM days WHERE LOWER(day_name)=LOWER(%s)", (day_name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute("INSERT INTO days (day_name) VALUES (%s)", (day_name,))
        return cursor.lastrowid

    # ---------------- CONFLICT CHECK ----------------
    def check_schedule_conflict(self, section_id, room_id, prof_id, day_id, start_time, end_time, cursor):
        """Check for section, room, and professor conflicts. Avoid comparing with itself during update."""

        current_id = getattr(self, "selected_schedule_id", None)

        conflicts = []

        # SECTION CONFLICT
        cursor.execute("""
            SELECT s.schedule_id, r.room_name,
                TIME_FORMAT(s.start_time, '%h:%i %p'),
                TIME_FORMAT(s.end_time, '%h:%i %p')
            FROM schedules s
            LEFT JOIN rooms r ON s.room_id = r.room_id
            WHERE s.section_id = %s
            AND s.day_id = %s
            AND (s.start_time < %s AND s.end_time > %s)
            AND (%s IS NULL OR s.schedule_id != %s)
        """, (section_id, day_id, end_time, start_time, current_id, current_id))
        section_conflict = cursor.fetchone()
        if section_conflict:
            conflicts.append(
                f"Section conflict: This section already has a schedule in room '{section_conflict[1]}' "
                f"from {section_conflict[2]} to {section_conflict[3]}."
            )

        # ROOM CONFLICT
        cursor.execute("""
            SELECT s.schedule_id, sec.section_name,
                TIME_FORMAT(s.start_time, '%h:%i %p'),
                TIME_FORMAT(s.end_time, '%h:%i %p')
            FROM schedules s
            LEFT JOIN sections sec ON s.section_id = sec.section_id
            WHERE s.room_id = %s
            AND s.day_id = %s
            AND (s.start_time < %s AND s.end_time > %s)
            AND (%s IS NULL OR s.schedule_id != %s)
        """, (room_id, day_id, end_time, start_time, current_id, current_id))
        room_conflict = cursor.fetchone()
        if room_conflict:
            conflicts.append(
                f"Room conflict: Room is already booked for section '{room_conflict[1]}' "
                f"from {room_conflict[2]} to {room_conflict[3]}."
            )

        # PROFESSOR CONFLICT
        cursor.execute("""
            SELECT s.schedule_id, sec.section_name,
                TIME_FORMAT(s.start_time, '%h:%i %p'),
                TIME_FORMAT(s.end_time, '%h:%i %p')
            FROM schedules s
            LEFT JOIN sections sec ON s.section_id = sec.section_id
            WHERE s.professor_id = %s
            AND s.day_id = %s
            AND (s.start_time < %s AND s.end_time > %s)
            AND (%s IS NULL OR s.schedule_id != %s)
        """, (prof_id, day_id, end_time, start_time, current_id, current_id))
        prof_conflict = cursor.fetchone()
        if prof_conflict:
            conflicts.append(
                f"Professor conflict: Assigned professor already teaches section '{prof_conflict[1]}' "
                f"from {prof_conflict[2]} to {prof_conflict[3]}."
            )

        # If ANY conflict exists — block saving
        if conflicts:
            messagebox.showerror("Schedule Conflict", "\n".join(conflicts))
            return True

        return False


    # ---------------- SAVE SCHEDULE ----------------
    def save_schedule(self):
        """Insert a new schedule with full conflict checks and safe FK creation."""
        if not self.validate_time():
            return

        inputs = {k: v.get().strip() for k, v in self.entries.items()}
        if not all(inputs.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        # prepare times: both TIME string for SQL comparison and time object for insert
        t_start_obj = datetime.strptime(inputs["Time Start"], "%I:%M %p").time()
        t_end_obj = datetime.strptime(inputs["Time End"], "%I:%M %p").time()
        t_start_str = datetime.strptime(inputs["Time Start"], "%I:%M %p").strftime("%H:%M:%S")
        t_end_str = datetime.strptime(inputs["Time End"], "%I:%M %p").strftime("%H:%M:%S")

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # get/create FKs in same transaction
            section_id, _ = self.get_or_create_section(inputs["Section"], inputs["Program"], cursor)
            course_id, _ = self.get_or_create_course(inputs["Course Code"], inputs["Course Name"], inputs["Program"], cursor)
            prof_id, _ = self.get_or_create_professor(inputs["Professor"], cursor)
            room_id, _ = self.get_or_create_room(inputs["Room"], cursor)
            day_id = self.get_or_create_day(inputs["Day"], cursor)

            # check conflicts (use HH:MM:SS strings)
            if self.check_schedule_conflict(section_id, room_id, prof_id, day_id, t_start_str, t_end_str, cursor):
                conn.rollback()
                return

            # insert schedule
            cursor.execute("""
                INSERT INTO schedules (section_id, course_id, professor_id, room_id, day_id, start_time, end_time)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (section_id, course_id, prof_id, room_id, day_id, t_start_obj, t_end_obj))

            conn.commit()
            messagebox.showinfo("Success", "Schedule saved successfully!")
            self.load_dropdowns_static()
            self.load_schedule_data()
            self.clear_fields()

        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Database Error", f"Failed to save schedule:\n{err}")
        finally:
            cursor.close()
            conn.close()

    # ---------------- UPDATE SCHEDULE ----------------
    def update_schedule(self):
        """Update an existing selected schedule (requires a row selected)."""
        if not self.selected_schedule_id:
            messagebox.showinfo("Select", "Please select a schedule from the table to update.")
            return

        if not self.validate_time():
            return

        inputs = {k: v.get().strip() for k, v in self.entries.items()}
        if not all(inputs.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        # prepare times
        t_start_obj = datetime.strptime(inputs["Time Start"], "%I:%M %p").time()
        t_end_obj = datetime.strptime(inputs["Time End"], "%I:%M %p").time()
        t_start_str = datetime.strptime(inputs["Time Start"], "%I:%M %p").strftime("%H:%M:%S")
        t_end_str = datetime.strptime(inputs["Time End"], "%I:%M %p").strftime("%H:%M:%S")

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # get/create fks (same transaction)
            section_id, _ = self.get_or_create_section(inputs["Section"], inputs["Program"], cursor)
            course_id, _ = self.get_or_create_course(inputs["Course Code"], inputs["Course Name"], inputs["Program"], cursor)
            prof_id, _ = self.get_or_create_professor(inputs["Professor"], cursor)
            room_id, _ = self.get_or_create_room(inputs["Room"], cursor)
            day_id = self.get_or_create_day(inputs["Day"], cursor)

    
            cursor.execute("""
                SELECT s.schedule_id, r.room_name, TIME_FORMAT(s.start_time, '%h:%i %p'), TIME_FORMAT(s.end_time, '%h:%i %p')
                FROM schedules s LEFT JOIN rooms r ON s.room_id = r.room_id
                WHERE s.section_id=%s AND s.day_id=%s AND (s.start_time < %s AND s.end_time > %s) AND s.schedule_id != %s
                LIMIT 1
            """, (section_id, day_id, t_end_str, t_start_str, self.selected_schedule_id))
            sec = cursor.fetchone()
            if sec:
                messagebox.showerror("Conflict", f"Section conflict — this section already has a schedule in room '{sec[1]}' from {sec[2]} to {sec[3]}.")
                conn.rollback()
                return

            # ROOM conflict excluding current id
            cursor.execute("""
                SELECT s.schedule_id, sec.section_name, TIME_FORMAT(s.start_time, '%h:%i %p'), TIME_FORMAT(s.end_time, '%h:%i %p')
                FROM schedules s LEFT JOIN sections sec ON s.section_id = sec.section_id
                WHERE s.room_id=%s AND s.day_id=%s AND (s.start_time < %s AND s.end_time > %s) AND s.schedule_id != %s
                LIMIT 1
            """, (room_id, day_id, t_end_str, t_start_str, self.selected_schedule_id))
            room = cursor.fetchone()
            if room:
                messagebox.showerror("Conflict", f"Room conflict — room is already booked for section '{room[1]}' from {room[2]} to {room[3]}.")
                conn.rollback()
                return

            # PROFESSOR conflict excluding current id
            cursor.execute("""
                SELECT s.schedule_id, sec.section_name, TIME_FORMAT(s.start_time, '%h:%i %p'), TIME_FORMAT(s.end_time, '%h:%i %p')
                FROM schedules s LEFT JOIN sections sec ON s.section_id = sec.section_id
                WHERE s.professor_id=%s AND s.day_id=%s AND (s.start_time < %s AND s.end_time > %s) AND s.schedule_id != %s
                LIMIT 1
            """, (prof_id, day_id, t_end_str, t_start_str, self.selected_schedule_id))
            prof = cursor.fetchone()
            if prof:
                messagebox.showerror("Conflict", f"Professor conflict — assigned professor already teaches section '{prof[1]}' from {prof[2]} to {prof[3]}.")
                conn.rollback()
                return

            # If no conflicts, perform update
            cursor.execute("""
                UPDATE schedules
                SET section_id=%s, course_id=%s, professor_id=%s, room_id=%s, day_id=%s, start_time=%s, end_time=%s
                WHERE schedule_id=%s
            """, (section_id, course_id, prof_id, room_id, day_id, t_start_obj, t_end_obj, self.selected_schedule_id))

            conn.commit()
            messagebox.showinfo("Success", "Schedule updated successfully!")
            self.load_dropdowns_static()
            self.load_schedule_data()
            self.clear_fields()

        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Database Error", f"Failed to update schedule:\n{err}")
        finally:
            cursor.close()
            conn.close()

    def update_schedule(self):
            """Update the selected schedule only if no conflicts exist."""
            if not self.selected_schedule_id:
                messagebox.showinfo("Select", "Please select a schedule from the table to update.")
                return

            if not self.validate_time():
                return

            inputs = {k: v.get().strip() for k, v in self.entries.items()}
            if not all(inputs.values()):
                messagebox.showerror("Error", "All fields are required.")
                return

            # prepare times
            t_start_obj = datetime.strptime(inputs["Time Start"], "%I:%M %p").time()
            t_end_obj = datetime.strptime(inputs["Time End"], "%I:%M %p").time()
            t_start_str = datetime.strptime(inputs["Time Start"], "%I:%M %p").strftime("%H:%M:%S")
            t_end_str = datetime.strptime(inputs["Time End"], "%I:%M %p").strftime("%H:%M:%S")

            conn = connect_db()
            cursor = conn.cursor()

            try:
                # get or create foreign keys
                section_id, _ = self.get_or_create_section(inputs["Section"], inputs["Program"], cursor)
                course_id, _ = self.get_or_create_course(inputs["Course Code"], inputs["Course Name"], inputs["Program"], cursor)
                prof_id, _ = self.get_or_create_professor(inputs["Professor"], cursor)
                room_id, _ = self.get_or_create_room(inputs["Room"], cursor)
                day_id = self.get_or_create_day(inputs["Day"], cursor)

                # CHECK CONFLICTS (exclude current schedule)
                if self.check_schedule_conflict(section_id, room_id, prof_id, day_id, t_start_str, t_end_str, cursor):
                    conn.rollback()
                    return

                # If no conflicts, perform update
                cursor.execute("""
                    UPDATE schedules
                    SET section_id=%s, course_id=%s, professor_id=%s, room_id=%s, day_id=%s, start_time=%s, end_time=%s
                    WHERE schedule_id=%s
                """, (section_id, course_id, prof_id, room_id, day_id, t_start_obj, t_end_obj, self.selected_schedule_id))

                conn.commit()
                messagebox.showinfo("Success", "Schedule updated successfully!")
                self.load_dropdowns_static()
                self.load_schedule_data()
                self.clear_fields()

            except mysql.connector.Error as err:
                conn.rollback()
                messagebox.showerror("Database Error", f"Failed to update schedule:\n{err}")
            finally:
                cursor.close()
                conn.close()


    # ---------------- DELETE SCHEDULE ----------------
    def delete_schedule(self):
        if not self.selected_schedule_id:
            messagebox.showinfo("Select", "Please select a schedule from the table to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected schedule?"):
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM schedules WHERE schedule_id=%s", (self.selected_schedule_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Schedule deleted.")
            self.load_schedule_data()
            self.clear_fields()

            # <-- ADD THIS LINE TO REFRESH DASHBOARD -->
            if hasattr(self.master, "load_dashboard_data"):
                self.master.load_dashboard_data()

        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Database Error", f"Failed to delete schedule:\n{err}")
        finally:
            cursor.close()
            conn.close()


    # ---------------- LOGOUT ----------------
    def logout(self):
        if self.switch_screen_callback:
            self.switch_screen_callback("login")

    # ---------------- DATETIME UPDATER ----------------
    def update_time(self):
        now = datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        self.datetime_label.config(text=now)
        self.after(1000, self.update_time)
