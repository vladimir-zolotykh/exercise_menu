#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import tkinter as tk
from PIL import Image, ImageTk
from register import Register

if __name__ == '__main__':
    root = tk.Tk()
    reg_frame = Register(root)
    reg_frame.grid(column=0, row=0, sticky=tk.NSEW)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()
