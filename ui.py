import sys
import tkinter as tk
from tkinter import ttk


class PGPKeys:
    PUB = 'public'
    PRIV = 'private'


class AppWin:
    def __init__(self):
        self.gen_pop = None
        self.confirm_gen_btn: ttk.Button = None
        self.style: ttk.Style = None
        self.upload_menu = None
        self.upload_btn = None
        self.gen_btn = None
        self.r_frame = None
        self.cmnt_entry = None
        self.cmnt_lbl = None
        self.email_entry = None
        self.email_lbl = None
        self.name_txt = None
        self.name_lbl = None
        self.l_frame = None

        self.w = 640
        self.h = 480
        self.win = tk.Tk()
        self.x_pos = int((self.win.winfo_screenwidth() / 2) - (self.w / 2))
        self.y_pos = int((self.win.winfo_screenheight() / 2) - (self.h / 2))
        self.win.geometry(f"{self.w}x{self.h}+{self.x_pos}+{self.y_pos}")

        self.win.protocol('WM_DELETE_WINDOW', self.shutdown)

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.cmnt_var = tk.StringVar()

        self.build()

    def shutdown(self):
        self.win.destroy()
        sys.exit(0)

    def build(self):
        self.style = ttk.Style()

        self.build_right_frame()

    def build_right_frame(self):
        self.r_frame = ttk.Frame(self.win, padding=10)
        self.r_frame.grid(row=0, column=1, sticky='nsew')

        self.gen_btn = ttk.Button(self.r_frame, text="generate key", command=self.open_gen_win)
        self.gen_btn.grid(row=0, column=0)

        self.upload_btn = ttk.Menubutton(self.r_frame, text="upload...")
        self.upload_menu = tk.Menu(self.upload_btn, tearoff=0)
        self.upload_menu.add_command(label="public key", command=lambda: self.upload_key())
        self.upload_menu.add_command(label="private key", command=lambda: self.upload_key(option=PGPKeys.PRIV))
        self.upload_btn.config(menu=self.upload_menu)
        self.upload_btn.grid(row=1, column=0, pady=5)

    def open_gen_win(self):
        self.gen_pop = tk.Toplevel(self.win)
        self.gen_pop.title('key generation tool')
        w = 340
        h = 180
        x_pos = int((self.win.winfo_screenwidth() / 2) - (w / 2)) + self.win.winfo_x()
        y_pos = int((self.win.winfo_screenheight() / 2) - (h / 2)) + self.win.winfo_y()
        self.gen_pop.geometry(f"{w}x{h}+{x_pos}+{y_pos}")

        self.name_lbl = ttk.Label(self.gen_pop, text='name')
        self.name_lbl.grid(row=0, column=0)

        self.name_txt = ttk.Entry(self.gen_pop, textvariable=self.name_var)
        self.name_txt.grid(row=0, column=1)

        self.email_lbl = ttk.Label(self.gen_pop, text='email')
        self.email_lbl.grid(row=1, column=0)

        self.email_entry = ttk.Entry(self.gen_pop, textvariable=self.email_var)
        self.email_entry.grid(row=1, column=1)

        self.cmnt_lbl = ttk.Label(self.gen_pop, text='comments')
        self.cmnt_lbl.grid(row=2, column=0)

        self.cmnt_entry = ttk.Entry(self.gen_pop, textvariable=self.cmnt_var)
        self.cmnt_entry.grid(row=2, column=1)

        ok = ttk.Button(self.gen_pop, text='ok', command=self.proc_gen_key, state=tk.DISABLED)
        ok.grid(row=3, column=0)
        cancel = ttk.Button(self.gen_pop, text='cancel', command=self.gen_pop.destroy)
        cancel.grid(row=3, column=1)

    def proc_gen_key(self):
        self.gen_pop.destroy()

    def run(self):
        self.win.mainloop()

    def upload_key(self, option=PGPKeys.PUB):
        pass


def main():
    app = AppWin()
    app.run()


if __name__ == "__main__":
    main()
