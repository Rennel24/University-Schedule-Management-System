import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance, ImageOps
from pathlib import Path

class WelcomeScreen(tk.Frame):
    """
    Welcome screen with background image lightly tinted red so
    the red theme remains visible while the image shows through.
    """

    BG_PATH = Path("assets/background.png")  # adjust if necessary

    def __init__(self, master, switch_screen_callback=None):
        super().__init__(master)
        self.master = master
        self.switch_screen_callback = switch_screen_callback

        # Make window full screen / maximized
        try:
            self.master.state("zoomed")
        except Exception:
            # fallback for platforms where "zoomed" isn't supported
            self.master.attributes("-zoomed", True)

        # placeholders for images
        self.bg_photo = None

        # Defer heavy image loading until widget is mapped and sizes are valid
        self.after(50, self._init_ui)

    def _init_ui(self):
        # Create widgets (placeholders). The background image will be applied after sizing.
        self._create_base_widgets()

        # Load and apply background (resized to current window size)
        self._load_and_apply_tinted_background()

        # Bind resize so the background updates if user resizes the window
        self.master.bind("<Configure>", self._on_master_configure)

    def _create_base_widgets(self):
        # Background label (image applied later)
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # MAIN CENTER CARD (white container)
        self.outer_frame = tk.Frame(self, bg="white", bd=0)
        self.outer_frame.place(relx=0.5, rely=0.5, anchor="center",
        relwidth=0.55, relheight=0.55)

        # Inner dark frame to simulate rounded-card effect
        self.inner_frame = tk.Frame(self.outer_frame, bg="#6e0a0a", bd=0)
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center",
        relwidth=0.93, relheight=0.88)

        # Title
        # Use common formal fonts; Tkinter will fallback if not present
        self.welcome_label = tk.Label(
            self.inner_frame,
            text="CAMPUS SCHEDULE\nMANAGEMENT SYSTEM",
            font=("Segoe UI", 40, "bold"),
            bg="#6e0a0a",
            fg="white",
            justify="center"
        )
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

        # NEXT Button (styled)
        self.next_button = tk.Button(
            self,
            text="Next",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#8B0000",
            activebackground="#f0f0f0",
            padx=12,
            pady=5,
            relief="flat",
            command=self.go_to_next,
            cursor="hand2"
        )
        self.next_button.place(relx=0.97, rely=0.95, anchor="se")
        self.next_button.bind("<Enter>", lambda e: self.next_button.config(bg="#f7f7f7"))
        self.next_button.bind("<Leave>", lambda e: self.next_button.config(bg="white"))

    def _load_and_apply_tinted_background(self):
        """Load image, resize to window, tint with red, and set as label image."""
        if not self.BG_PATH.exists():
            # if file missing, fill with solid color so UI stays usable
            self.bg_label.config(bg="#8B0000")
            return

        w = max(1, self.master.winfo_width())
        h = max(1, self.master.winfo_height())

        try:
            img = Image.open(self.BG_PATH).convert("RGBA")
        except Exception as e:
            # fallback to solid fill on error
            self.bg_label.config(bg="#8B0000")
            print("Failed to open background image:", e)
            return

        # Resize while preserving aspect ratio (cover)
        img = ImageOps.fit(img, (w, h), Image.LANCZOS)

        # Create a red overlay image and blend with original using alpha
        red_layer = Image.new("RGBA", img.size, (139, 0, 0, 255))  # #8B0000
        tint_alpha = 0.30  # 0.0 (no tint) .. 1.0 (solid red). adjust to taste
        blended = Image.blend(img, red_layer, tint_alpha)

        # Optionally slightly reduce brightness or increase contrast for a polished look
        # enhancer = ImageEnhance.Brightness(blended)
        # blended = enhancer.enhance(0.95)

        # Convert to PhotoImage and set it
        self.bg_photo = ImageTk.PhotoImage(blended)
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo  # keep reference to prevent GC

    def _on_master_configure(self, event):
        """Handle resize events: reload background if size changed significantly."""
        # Throttle rapid configure calls by using after_cancel/after
        if getattr(self, "_resize_after_id", None):
            self.after_cancel(self._resize_after_id)
        self._resize_after_id = self.after(120, self._load_and_apply_tinted_background)

    def go_to_next(self):
        if self.switch_screen_callback:
            self.switch_screen_callback("login")
