#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
# from collections import namedtuple
from types import MethodType
from typing import Any, NamedTuple
import re
import tkinter as tk
from PIL import Image, ImageTk
from scrolledcanvas import ScrolledCanvas
SIZE = (100, 100)
saved_photos = []
dirx = {name: Image.open(path).resize(SIZE)
        for name, path in zip(
                ("squat",
                 "bench press",
                 "deadlift",
                 "pullup",
                 "front squat",
                 "overhead standing press",
                 "biceps curl",
                 "back plank"),
                (os.path.expanduser("~/Downloads/squat.jpg"),
                 os.path.expanduser("~/Downloads/bench_press.jpg"),
                 os.path.expanduser("~/Downloads/deadlift.jpg"),
                 os.path.expanduser("~/Downloads/pullup.jpg"),
                 os.path.expanduser("~/Downloads/front_squat.jpg"),
                 os.path.expanduser("~/Downloads/overhead_press.jpg"),
                 os.path.expanduser("~/Downloads/biceps_curl.jpg"),
                 os.path.expanduser("~/Downloads/back_plank.jpg")))
        }


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

# ExerCash = namedtuple('ExerCash', "index image name image_id name_id")


class ExerCash(NamedTuple):
    index: int
    image: ImageTk.PhotoImage
    name: str
    image_id: int
    name_id: int


class ExerDir(list[ExerCash]):
    def findexerby_id(self, *, image_id, name_id):
        for ex in self:
            if ex.image_id == image_id or ex.name_id == name_id:
                return ex
        raise TypeError(f'Exercise with '
                        f'{image_id} == {image_id} or {name_id} == {name_id}'
                        f' not found')

    def find_name(self, name: str) -> ExerCash:
        # name: 'bench press (1)'
        requested_name = name
        if  (m := re.match('(?P<exer_name>.*) \(\d+\)', name)):
            requested_name = m.group('exer_name')
        for exer in self:
            if requested_name == exer.name:
                return exer
        raise TypeError(f'Exercise {name} not found')


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
        # self.exercises: list[ExerCash] = []
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        item = self.find_closest(event.x, event.y)
        try:
            exer_name = self.itemcget(item[0], 'text')
            self.selected_exer = self.exercises.find_name(exer_name)
            if self.menu:
                MethodType(_change_label, self.menu)(self.selected_exer.name)
        except tk.TclError:
            print('Not a text clicked')

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
