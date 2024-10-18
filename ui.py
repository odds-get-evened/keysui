import tkinter as tk
from tkinter import ttk


class AppWin:
    def __init__(self):
        self.confirm_gen_btn: ttk.Button = None
        self.style: ttk.Style = None
        self.upload_menu = None
        self.upload_btn = None
        self.gen_button = None
        self.r_frame = None
        self.cmnt_entry = None
        self.cmnt_label = None
        self.email_entry = None
        self.email_label = None
        self.name_txt = None
        self.name_lbl = None
        self.l_frame = None

        self.w = 640
        self.h = 480
        self.win = tk.Tk()
        self.x_pos = int((self.win.winfo_screenwidth() / 2) - (self.w / 2))
        self.y_pos = int((self.win.winfo_screenheight() / 2) - (self.h / 2))
        self.win.geometry(f"{self.w}x{self.h}+{self.x_pos}+{self.y_pos}")

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.cmnt_var = tk.StringVar()

        self.build()

    def build(self):
        self.style = ttk.Style()

        self.build_right_frame()

    def build_right_frame(self):
        self.r_frame = ttk.Frame(self.win, padding=10)
        self.r_frame.grid(row=0, column=1, sticky='nsew')

        self.gen_button = ttk.Button(self.r_frame, text="generate key", command=self.generate_key)
        self.gen_button.grid(row=0, column=0)

        self.upload_btn = ttk.Menubutton(self.r_frame, text="upload...")
        self.upload_menu = tk.Menu(self.upload_btn, tearoff=0)
        self.upload_menu.add_command(label="public key", command=lambda: self.upload_key())
        self.upload_menu.add_command(label="private key", command=lambda: self.upload_key(option='private'))
        self.upload_btn.config(menu=self.upload_menu)
        self.upload_btn.grid(row=1, column=0, pady=5)

    def generate_key(self):
        # enable text entry
        self.cmnt_entry.config(state=tk.NORMAL)

    def run(self):
        self.win.mainloop()

    def upload_key(self, option='public'):
        pass


def main():
    app = AppWin()
    app.run()


if __name__ == "__main__":
    main()
