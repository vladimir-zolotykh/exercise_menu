#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
from typing import Union
from dataclasses import dataclass
from PIL import Image as Image_mod
from PIL import ImageTk
import re
saved_photos: list[ImageTk.PhotoImage] = []


@dataclass
class Row3:
    row: int | None = None      # canvas row number
    image_id: int | None = None
    name_id: int | None = None


@dataclass
class Lift:
    name: str                   # 'squat' or 'bench press'
    image: ImageTk.PhotoImage
    visible: bool = False
    row3: Row3 = Row3()

    def hide(self):
        self.visible = False
        self.row3 = Row3()

    def show(self, row3: Row3):
        self.visible = True
        self.row3 = row3
    

class Lifts(dict[str, Lift]):
    def add(self, lift_name: str, image_dir: str | None) -> Lift:
        if image_dir is None:
            image_dir = os.path.expanduser('~/Downloads/')
        if lift_name not in self:
            image = Image_mod.open(os.path.join(
                image_dir, f"{lift_name.replace(' ', '_')}.jpg"))
            photo = ImageTk.PhotoImage(image)
            saved_photos.append(photo)
            self[lift_name] = Lift(lift_name, photo)
        return self[lift_name]

    def find(
            self, *, name: str = '', name_id: int = -1, image_id: int = -1
    ) -> Lift | None:
        if name:
            if  (m := re.match('(?P<exer_name>.*)( \(\d+\))?', name)):
                name = m.group('exer_name')
        k: str
        v: Lift
        for k, v in self.items():
            if name == k or (name_id == v.row3.name_id and
                             image_id == v.row3.image_id):
                return v
        return None

    def hide(self, name: str):
        lift = self[name]
        lift.hide()

    def show(self, name: str, row3: Row3):
        lift = self[name]
        lift.show(row3)

