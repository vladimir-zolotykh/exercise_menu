#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from PIL import Image, ImageTk
from scrolledcanvas import ScrolledCanvas
SIZE = (50, 50)
saved_photos = []
dirx = {name: Image.open(path).resize(SIZE)
        for name, path in zip(
                ("bench press", "squat", "deadlift"),
                ("/usr/share/plymouth/debian-logo.png",
                 "/usr/share/evolution/images/working.png",
                 "/usr/share/help/C/five-or-more/figures/medium.png"))}


class Register(ScrolledCanvas):
    def __init__(self, owner, **kwargs):
        kwargs.update({'scrollregion': (0, 0, 200, 150)})
        super().__init__(owner, **kwargs)
        self._x = 0
        self._y = 0

    def append(self, *, image=None, name=''):
        self.create_image(self._x, self._y, image=image, anchor=tk.NW)
        self.create_text(self._x + SIZE[0], self._y, text=name, anchor=tk.NW)
        self._y += SIZE[1]


class RegisterFrame(tk.Frame):
    def __init__(self, owner):
        super().__init__(owner)
        canvas = Register(self)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
        for name, img in dirx.items():
            saved_photos.append(ImageTk.PhotoImage(img))
            canvas.append(image=saved_photos[-1], name=name)
