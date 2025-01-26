#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
# from collections import namedtuple
from types import MethodType
from typing import Any, NamedTuple, Callable
import re
from itertools import dropwhile
import tkinter as tk
from PIL import Image, ImageTk
from scrolledcanvas import ScrolledCanvas
# SIZE = (90, 160)
SIZE = (45, 80)
saved_photos = []
EXER_LIST = ("squat", "bench press", "deadlift", "pullup", "front squat",
             "overhead press","biceps curl", "back plank")
dirx = {}
try:
    dirx = {
        name: Image.open(path).resize(SIZE)
        for name, path in zip(
                EXER_LIST,
                (os.path.expanduser(f'~/Downloads/{xn.replace(" ", "_")}.jpg')
                 for xn in EXER_LIST))
    }
except FileNotFoundError as e:
    print(f'{e.filename}: file not found')
    exit(1)


class Register(ScrolledCanvas):
    def __init__(self, owner, **kwargs):
        super().__init__(owner, **kwargs)
        self._x = 0
        self._y = 0

    def append(self, *, image=None, name='', exer_id=0):
        image_id = self.create_image(
            self._x, self._y, image=image, anchor=tk.NW)
        name_id = self.create_text(self._x + SIZE[0], self._y,
                                   text=f'{name} ({exer_id})', anchor=tk.NW)
        self._y += SIZE[1]
        return image_id, name_id


class ExerCash(NamedTuple):
    index: int
    image: ImageTk.PhotoImage
    name: str
    image_id: int
    name_id: int


class ExerDir(list[ExerCash]):
    def find_exer(
            self, *, name: str = '', image_id: int = 0, name_id: int = 0
    ) -> ExerCash:
        err: TypeError
        predicate: Callable[[ExerDir], bool] = lambda exer: False
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
    for index in range(self.index(tk.END)):
        if self.entrycget(index, 'label').startswith('Delete exercise'):
            self.entryconfig(index, label=f'Delete exercise <{exer_name}>')
            return
    raise TypeError('No "Delete exercise item" found')


class RegisterCash(Register):
    def __init__(self, owner, *, menu, **kwargs):
        super().__init__(owner, **kwargs)
        self.index = 1
        self.selected_exer: ExerCash = []
        self.exercises: ExerDir = ExerDir([])
        if menu:
            self.menu = menu
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        item = self.find_closest(self.canvasx(event.x), self.canvasy(event.y))
        try:
            self.selected_exer = self.exercises.find_exer(
                image_id=item[0], name_id=item[0])
            if self.menu:
                MethodType(_change_label, self.menu)(self.selected_exer.name)
        except tk.TclError:
            print('Not a text clicked')

    def refresh(self):
        for item in self.find_all():
            if self.type(item) in ('image', 'text'):
                self.delete(item)
        for exer_cash in self.exercises:
            super().append(image=exer_cash.image, name=exer_cash.name)

    def append(self, *, image=None, name=''):
        image_id, name_id = super().append(
            image=image, name=name, exer_id=self.index)
        self.exercises.append(ExerCash(
            self.index, image, name, image_id, name_id))
        self.index += 1

class RegisterFrame(tk.Frame):
    def __init__(self, owner, *, menu):
        super().__init__(owner)
        canvas = RegisterCash(self, menu=menu)
        canvas.grid(column=0, row=0, sticky=tk.NSEW)
        for name, img in dirx.items():
            saved_photos.append(ImageTk.PhotoImage(img))
            canvas.append(image=saved_photos[-1], name=name)
        canvas.configure(scrollregion = canvas.bbox("all"))
