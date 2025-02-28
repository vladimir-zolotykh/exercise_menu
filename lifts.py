#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
from typing import Union, Optional, TypedDict
from dataclasses import dataclass
from PIL import Image as Image_mod
from PIL import ImageTk
import re
saved_photos: list[ImageTk.PhotoImage] = []

@dataclass
class SelectRect:
    # x0, y0, x1, y1, ...
    coord: list[float] = field(default_factory=list)
    # line_id = canv.create_line()
    line_id: Optional[int] = None
    # 'background', 'lightblue'
    fill: Optional[str] = None

# highlighted rectangle around selected exercise
select_rect: SelectRect = SelectRect()

class FindArgs(TypedDict, total=False):
    name: str
    image_id: int
    name_id: int

@dataclass
class Canv3:
    """Extra attributes of a Lift

    related to a canvas if the Lift is present in the canvas
    """
    row: int | None = None      # canvas row numberыи
    image_id: int | None = None
    name_id: int | None = None


@dataclass
class Lift:
    name: str                   # 'squat' or 'bench press'
    image: ImageTk.PhotoImage
    visible: bool = False
    canv3: Canv3 = Canv3()

    def hide(self):
        self.visible = False
        self.canv3 = Canv3()

    # def show(self, canv3: Canv3):
    #     self.visible = True
    #     self.canv3 = canv3
    

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
            if name == k or (name_id == v.canv3.name_id and
                             image_id == v.canv3.image_id):
                return v
        return None

    def hide(self, name: str):
        lift = self[name]
        lift.hide()

    def show(self, name: str, canv3: Canv3):
        lift = self[name]
        lift.show(canv3)

