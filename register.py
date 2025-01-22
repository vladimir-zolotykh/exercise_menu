#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import namedtuple
import tkinter as tk
from PIL import Image, ImageTk
from scrolledcanvas import ScrolledCanvas
SIZE = (50, 50)
saved_photos = []
dirx = {name: Image.open(path).resize(SIZE)
        for name, path in zip(
                ("bench press", "squat", "deadlift",
                 "pullup", "front squat", "overhead standing press"),
                ("/usr/share/plymouth/debian-logo.png",
                 "/usr/share/evolution/images/working.png",
                 "/usr/share/help/C/five-or-more/figures/medium.png",
                 "/usr/share/plymouth/debian-logo.png",
                 "/usr/share/evolution/images/working.png",
                 "/usr/share/help/C/five-or-more/figures/medium.png"))}


class Register(ScrolledCanvas):
    def __init__(self, owner, **kwargs):
        super().__init__(owner, **kwargs)
        self._x = 0
        self._y = 0

    def append(self, *, image=None, name=''):
        image_id = self.create_image(
            self._x, self._y, image=image, anchor=tk.NW)
        name_id = self.create_text(
            self._x + SIZE[0], self._y, text=name, anchor=tk.NW)
        self._y += SIZE[1]
        return image_id, name_id

ExerCash = namedtuple('ExerCash', "index image name image_id name_id")


class RegisterCash(Register):
    def __init__(self, owner, **kwargs):
        super().__init__(owner, **kwargs)
        self.index = 0
        self.exercises: list[ExerCash] = []

    def refresh(self):
        for item in self.find_all():
            if self.type(item) in ('image', 'text'):
                self.delete(item)
        # for exer_cash in self.exercises:
        #     self.delete(exer_cash.image_id)
        #     self.delete(exer_cash.name_id)
        for exer_cash in self.exercises:
            super().append(image=exer_cash.image, name=exer_cash.name)

    def append(self, *, image=None, name=''):
        image_id, name_id = super().append(image=image, name=name)
        self.exercises.append(ExerCash(
            self.index, image, name, image_id, name_id))
        self.index += 1

class RegisterFrame(tk.Frame):
    def __init__(self, owner):
        super().__init__(owner)
        canvas = RegisterCash(self)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
        for name, img in dirx.items():
            saved_photos.append(ImageTk.PhotoImage(img))
            canvas.append(image=saved_photos[-1], name=name)
        canvas.configure(scrollregion = canvas.bbox("all"))
