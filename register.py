#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
# from collections import namedtuple
from types import MethodType
from dataclasses import dataclass
from typing import Optional, Any, Callable
import re
from itertools import dropwhile
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from scrolledcanvas import ScrolledCanvas
IMG_SIZE = (90, 160)
saved_photos = []
EXER_LIST = ("squat", "bench press", "deadlift", "pullup", "front squat",
             "overhead press","biceps curl", "back plank")
dirx = {}
try:
    dirx = {
        name: Image.open(path).resize(IMG_SIZE)
        for name, path in zip(
                EXER_LIST,
                (os.path.expanduser(f'~/Downloads/{xn.replace(" ", "_")}.jpg')
                 for xn in EXER_LIST))
    }
except FileNotFoundError as e:
    print(f'{e.filename}: file not found')
    exit(1)


class Register(ScrolledCanvas):
    def __init__(self, owner: tk.Widget, **kwargs: dict[str, Any]):
        super().__init__(owner, **kwargs)
        self._row: int = 0
        self._x = 0
        self._y = 0

    def toggle_selection_rect(self):
        x0, y0 = self._x, self._y
        x1 = x0 + 250  # len(ex_str) * 10
        y1 = y0 + IMG_SIZE[1]
        self.create_line(x0, y0, x1, y0, x1, y1, x0, y1, width=4,
                         fill='lightblue')

    def append(self, *, image=None, name='', exer_id=0):
        ex_str = f'{name} ({exer_id})'
        # self.toggle_selection_rect()
        image_id = self.create_image(
            self._x, self._y, image=image, anchor=tk.NW)
        name_id = self.create_text(self._x + IMG_SIZE[0], self._y,
                                   text=ex_str, anchor=tk.NW)

        def font_metrics() -> tuple[int, int]:
            name: str = self.itemcget(name_id, 'font') # 'TkDefaultFont'
            font = tkfont.nametofont(name)
            width = font.measure(ex_str) // len(ex_str)
            height = font.metrics("linespace")
            # font_width = 6, font_height = 17
            return width, height

        font_metrics()
        self._y += IMG_SIZE[1]
        return image_id, name_id


@dataclass
class ExerCash:
    index: int                  # exercise number or canvas row
    image: ImageTk.PhotoImage
    name: str                   # 'squat' or 'bench press'
    image_id: int               # canvas image id (exer. pic)
    name_id: int                # canvas text id (exer. name)


class ExerDir(list[ExerCash]):
    def find_exer(
            self, *, name: str = '', image_id: int = 0, name_id: int = 0
    ) -> ExerCash:
        err: TypeError
        predicate: Callable[[ExerCash], bool] = lambda exer: False
        if name:
            requested_name = name
            if  (m := re.match('(?P<exer_name>.*) \(\d+\)', name)):
                requested_name = m.group('exer_name')
                predicate = lambda exer: exer.name != requested_name
            err = TypeError(f'Exercise {requested_name} not found')
        elif image_id or name_id:
            predicate = lambda exer: (exer.image_id != image_id and
                                      exer.name_id != name_id)
            err = TypeError(
                f'Exercise with '
                f'{image_id} == {image_id} or {name_id} == {name_id}'
                f' not found')
        else:
            raise TypeError('Specify name, image_id, or name_id')
        try:
            return next(dropwhile(predicate, self))
        except StopIteration:
            raise err


def _change_label(self, exer_name):
    for item in range(self.index(tk.END)):
        if self.entrycget(item, 'label').startswith('Delete exercise'):
            self.entryconfig(item, label=f'Delete exercise <{exer_name}>')
            return
    raise TypeError('No "Delete exercise item" found')


class RegisterCash(Register):
    def __init__(
            self, owner: tk.Widget, *, menu: tk.Menu, **kwargs: dict[str, Any]
    ):
        super().__init__(owner, **kwargs)
        self.exer_i = 1
        self.selected_exer: Optional[ExerCash] = None
        self.exercises = ExerDir([])
        # self.selected_exer: ExerCash = []
        # self.exercises: ExerDir = ExerDir([])
        if menu:
            self.menu = menu
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        item = self.find_closest(self.canvasx(event.x), self.canvasy(event.y))
        ex = self.selected_exer
        if ex:
            self.itemconfig(ex.name_id, fill='black')
        if (ex := self.exercises.find_exer(image_id=item[0],
                                            name_id=item[0])):
            self.selected_exer = ex
        # ex = self.selected_exer = self.exercises.find_exer(
        #     image_id=item[0], name_id=item[0])
        self.itemconfig(ex.name_id, fill='lightblue')
        if self.menu:
            MethodType(_change_label, self.menu)(ex.name)

    def refresh(self):
        for item in self.find_all():
            if self.type(item) in ('image', 'text'):
                self.delete(item)
        for exer_cash in self.exercises:
            super().append(image=exer_cash.image, name=exer_cash.name)

    def append(self, *, image=None, name=''):
        image_id, name_id = super().append(
            image=image, name=name, exer_id=self.exer_i)
        self.exercises.append(ExerCash(
            self.exer_i, image, name, image_id, name_id))
        self.exer_i += 1

class RegisterFrame(tk.Frame):
    def __init__(self, owner, *, menu):
        super().__init__(owner)
        canvas = RegisterCash(self, menu=menu)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
        for name, img in dirx.items():
            saved_photos.append(ImageTk.PhotoImage(img))
            canvas.append(image=saved_photos[-1], name=name)
        canvas.configure(scrollregion = canvas.bbox("all"))
