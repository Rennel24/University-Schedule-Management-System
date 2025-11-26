import tkinter as tk
from screens.welcome_screen import WelcomeScreen
from screens.login_screen import LoginScreen  
from screens.dashboard_module import DashboardScreen
from screens.schedule_module import ScheduleScreen  

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Campus Schedule Management System")
        self.geometry("1200x700")
        self.configure(bg="#B22222")

        self.current_screen = None
        self.show_welcome_screen()

    # ----------------- SHOW SCREENS -----------------
    def show_welcome_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = WelcomeScreen(self, self.switch_screen)
        self.current_screen.pack(fill="both", expand=True)

    def show_login_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = LoginScreen(self, self.switch_screen)
        self.current_screen.pack(fill="both", expand=True)

    def show_dashboard_screen(self, admin_data=None):
        from screens.dashboard_module import DashboardScreen  # Now works
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = DashboardScreen(
            self,
            switch_screen_callback=self.switch_screen,
            admin_data=admin_data
        )
        self.current_screen.pack(fill="both", expand=True)

    def show_schedule_screen(self, admin_data=None):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = ScheduleScreen(
            self,
            switch_screen_callback=self.switch_screen,
            admin_data=admin_data
        )
        self.current_screen.pack(fill="both", expand=True)

    # ----------------- SWITCH SCREENS -----------------
    def switch_screen(self, screen_name, admin_data=None):
        if screen_name == "welcome":
            self.show_welcome_screen()
        elif screen_name == "login":
            self.show_login_screen()
        elif screen_name == "dashboard":
            self.show_dashboard_screen(admin_data)
        elif screen_name == "schedule":
            self.show_schedule_screen(admin_data)

if __name__ == "__main__":
    app = App()
    app.mainloop()
