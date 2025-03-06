#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
from typing import Union, Optional, TypedDict
from dataclasses import dataclass, field
from PIL import Image as Image_mod
from PIL import ImageTk
import re
import geometry as G
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
class Lift:
    name: str                   # 'squat' or 'bench press'
    image: ImageTk.PhotoImage
    visible: bool = False
    # the attributes below are valid if visible is True
    row: int | None = None      # canvas row
    image_id: int | None = None
    name_id: int | None = None
    

class Lifts(dict[str, Lift]):
    def add(self, lift_name: str, image_dir: str | None = None) -> Lift:
        if image_dir is None:
            image_dir = os.path.expanduser('~/Downloads/')
        if lift_name not in self:
            image = Image_mod.open(os.path.join(
                image_dir,
                f"{lift_name.replace(' ', '_')}.jpg")).resize(G.IMAGE)
            photo = ImageTk.PhotoImage(image)
            saved_photos.append(photo)
            self[lift_name] = Lift(lift_name, photo)
            self[lift_name].visible = False
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
            if name == k or (name_id == v.name_id and
                             image_id == v.image_id):
                return v
        return None
