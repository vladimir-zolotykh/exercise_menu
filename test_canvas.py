#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from PIL import Image, ImageTk
SIZE = (50, 50)
dirx = {name: Image.open(path).resize(SIZE)
        for name, path in zip(
                ("bench press", "squat", "deadlift"),
                ("/usr/share/plymouth/debian-logo.png",
                 "/usr/share/evolution/images/working.png",
                 "/usr/share/help/C/five-or-more/figures/medium.png"))}


if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root)
    canvas.grid(column=0, row=0, sticky=tk.NSEW)
    x = y = 0
    _saved = []
    for name, img in dirx.items():
        _saved.append(ImageTk.PhotoImage(img))
        canvas.create_image(x, y, image=_saved[-1], anchor=tk.NW)
        canvas.create_text(x + SIZE[0], y, text=name, anchor=tk.NW)
        y += SIZE[1]
    tk.mainloop()
