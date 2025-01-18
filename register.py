#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from PIL import Image, ImageTk

exer_list = ["squat", "bench press", "deadlift"]
exer_pics = [
    "/usr/share/evolution/images/working.png",
    "/usr/share/plymouth/debian-logo.png",
    "/usr/share/help/C/five-or-more/figures/medium.png"
]
_loaded_images = []


def get_exer_image(exer_id, exer_pics):
    img_png = exer_pics[exer_id]
    image = Image.open(exer_pics[exer_id])
    image = image.resize((50, 50))
    _loaded_images.append(ImageTk.PhotoImage(image))
    return _loaded_images[-1]


class Register(tk.Frame):
    def __init__(self, parent):
        self._parent = parent
        super().__init__(parent)
        row = 0
        for exer_id, exer_name in enumerate(exer_list):
            exer_img = tk.Label(self, image=get_exer_image(exer_id, exer_pics),
                                text=exer_name)
            exer_img.grid(column=0, row=row)
            exer_lab = tk.Label(self, text=exer_name)
            exer_lab.grid(column=1, row=row)
            row += 1
    
