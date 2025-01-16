#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import tkinter as tk
from PIL import Image, ImageTk

if __name__ == '__main__':
    root = tk.Tk()
    image = Image.open(os.path.expanduser(
        "~/Downloads/Screenshot_20250115-191509_Gallery.jpg"))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    label.pack()
    root.mainloop()
