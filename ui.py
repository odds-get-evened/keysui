import dbm
import hashlib
import os.path
import re
import sys
import tkinter as tk
import warnings
from pathlib import Path
from tkinter import ttk, filedialog, messagebox

import pgpy
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm


class PGPKeys:
    PUB = 'public'
    PRIV = 'private'


class KeyStuff:
    @classmethod
    def generate_key(cls, name, email, comment='', protect=False):
        warnings.filterwarnings('ignore')  # because PGPy dev put warnings in code print
        key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
        uid = pgpy.PGPUID.new(name.strip(), comment=comment, email=email)
        key.add_uid(
            uid,
            usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA512],
            ciphers=[SymmetricKeyAlgorithm.AES256],
            compression=[
                CompressionAlgorithm.ZLIB,
                CompressionAlgorithm.BZ2,
                CompressionAlgorithm.ZIP
            ]
        )

        if protect:
            # use hashed comment as password
            passwd = hashlib.sha256(comment.strip().encode()).hexdigest()
            key.protect(passwd, SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)

        return key


class DBStuff:
    DB_PATH = Path(os.path.expanduser('~'), '.databox', 'keysui', 'storage')

    @classmethod
    def check(cls):
        if not cls.DB_PATH.parent.exists():
            cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def insert_key(cls, key: pgpy.PGPKey):
        cls.check()
        with dbm.open(cls.DB_PATH.__str__(), 'c') as db:
            h = hashlib.sha256().hexdigest()
            db[h] = key.__str__()
        print(f"key [{h}] successfully stored.")


class AppWin:
    PAD5 = 5

    def __init__(self):
        self.gen_ok_btn = None
        self.gen_pop = None
        self.confirm_gen_btn: ttk.Button = None
        self.style: ttk.Style = None
        self.upload_menu = None
        self.upload_btn = None
        self.gen_btn = None
        self.r_frame = None
        self.cmnt_txt = None
        self.cmnt_lbl = None
        self.email_txt = None
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

    def open_gen_win(self):
        self.gen_pop = tk.Toplevel(self.win)
        self.gen_pop.title('key generation tool')
        w = 340
        h = 180
        self.gen_pop.minsize(w, h)
        x_pos = int(self.win.winfo_x() + (w / 2))
        y_pos = int(self.win.winfo_y() + (h / 2))
        self.gen_pop.geometry(f"{w}x{h}+{x_pos}+{y_pos}")

        c = ttk.Frame(self.gen_pop)
        c.grid(sticky='nsew', padx=10, pady=10)

        self.name_lbl = ttk.Label(c, text='name', style='C.TLabel')
        self.name_lbl.grid(row=0, column=0, pady=AppWin.PAD5)

        bb = ttk.Frame(c)
        bb.grid(row=3, column=0, sticky='ew', columnspan=2, pady=AppWin.PAD5)
        self.gen_ok_btn = ttk.Button(bb, text='ok', command=self.proc_gen_key, state=tk.DISABLED)

        self.name_txt = ttk.Entry(c, textvariable=self.name_var)
        self.name_txt.bind('<KeyRelease>', self.validate_gen_key)
        self.name_txt.grid(row=0, column=1, sticky='ew', pady=AppWin.PAD5)

        self.email_lbl = ttk.Label(c, text='email')
        self.email_lbl.grid(row=1, column=0, pady=5)

        self.email_txt = ttk.Entry(c, textvariable=self.email_var)
        self.email_txt.bind('<KeyRelease>', self.validate_gen_key)
        self.email_txt.grid(row=1, column=1, sticky='ew', pady=AppWin.PAD5)

        self.cmnt_lbl = ttk.Label(c, text='comments')
        self.cmnt_lbl.grid(row=2, column=0, pady=AppWin.PAD5)

        self.cmnt_txt = ttk.Entry(c, textvariable=self.cmnt_var)
        self.cmnt_txt.grid(row=2, column=1, sticky='ew')

        self.gen_pop.grid_columnconfigure(0, weight=1)
        c.grid_columnconfigure(1, weight=1)

        self.gen_ok_btn.grid(row=0, column=0)
        cancel = ttk.Button(bb, text='cancel', command=self.gen_pop.destroy)
        cancel.grid(row=0, column=1)

    def proc_gen_key(self):
        name = self.name_var.get()
        email = self.email_var.get()
        comment = self.cmnt_var.get()

        key = KeyStuff.generate_key(name, email, comment=comment, protect=True)
        # add key to user's local database
        DBStuff.insert_key(key)

        self.gen_pop.destroy()

    def run(self):
        try:
            self.win.mainloop()
        except KeyboardInterrupt:
            self.shutdown()

    def validate_gen_key(self, evt: tk.Event = None):
        name = self.name_var.get()
        email = self.email_var.get()
        comment = self.cmnt_var.get()
        print(f"{name}; {email}; {comment}")

        is_name_valid = len(name.strip()) >= 3
        is_email_valid = re.match(
            r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
            email.strip())

        if is_email_valid and is_name_valid:
            self.gen_ok_btn.configure(state=tk.NORMAL)
        else:
            self.gen_ok_btn.configure(state=tk.DISABLED)


def main():
    app = AppWin()
    app.run()


if __name__ == "__main__":
    main()
