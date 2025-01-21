#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from PIL import Image, ImageTk
from scrolledcanvas import grid_expand
from register import Register

SIZE = (50, 50)
dirx = {name: Image.open(path).resize(SIZE)
        for name, path in zip(
                ("bench press", "squat", "deadlift"),
                ("/usr/share/plymouth/debian-logo.png",
                 "/usr/share/evolution/images/working.png",
                 "/usr/share/help/C/five-or-more/figures/medium.png"))}


if __name__ == '__main__':
    root = tk.Tk()
    grid_expand(root)
    canvas = Register(root)
    canvas.grid(column=0, row=0, sticky=tk.NSEW)
    _saved = []
    for name, img in dirx.items():
        _saved.append(ImageTk.PhotoImage(img))
        canvas.append(image=_saved[-1], name=name)
    tk.mainloop()
