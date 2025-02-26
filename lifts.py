#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
from typing import Union
from dataclasses import dataclass
from PIL import Image as Image_mod
from PIL import ImageTk
saved_photos: list[ImageTk.PhotoImage] = []


@dataclass
class Row3:
    row: int | None = None
    image_id: int | None = None
    name_id: int | None = None


@dataclass
class Lift:
    name: str                   # 'squat' or 'bench press'
    image: ImageTk.PhotoImage
    visible: bool = False
    # `visible' False means that the fields below are all not set
    row: int | None = None      # canvas row for the lift
    image_id: int | None = None # canvas's image id
    name_id: int | None = None  # canvas's text id

    def hide(self):
        self.visible = False
        self.row = self.image_id = self.name_id = None

    def show(self, row, image_id, name_id):
        self.visible = True
        self.row, self.image_id, self.name_id = (row, image_id, name_id)
    

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

    def hide(self, name: str):
        lift = self[name]
        lift.hide()

    def show(self, name: str, row, image_id, name_id):
        lift = self[name]
        lift.show(row, image_id, name_id)

