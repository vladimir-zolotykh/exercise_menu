#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from PIL import Image, ImageTk
exer_names = ["bench press", "squat", "deadlift"]
exer_pics = [
    "/usr/share/plymouth/debian-logo.png",
    "/usr/share/evolution/images/working.png",
    "/usr/share/help/C/five-or-more/figures/medium.png"
]
name_pic_zip = zip(exer_names, exer_pics)
_loaded_images = []


def get_exer_image(exer_id, exer_pics):
    try:
        return _loaded_images[exer_id]
    except:
        img_png = exer_pics[exer_id]
        image = Image.open(exer_pics[exer_id])
        image = image.resize((50, 50))
        _loaded_images.append(ImageTk.PhotoImage(image))
        return _loaded_images[-1]


if __name__ == '__main__':
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.grid(sticky=tk.NSEW)
    canvas = tk.Canvas(root)
    canvas.grid(column=0, row=0, sticky=tk.NSEW)
    canvas_row = 0
    # x = 25
    x = 0
    # y = 25
    y = 0
    for name, pic in name_pic_zip:
        print(f'{name = }, {y = }')
        img = get_exer_image(canvas_row, exer_pics)
        canvas.create_image(x, y, image=img, anchor=tk.NW)
        canvas.create_text(x + 50, y, text=name, anchor=tk.NW)
        canvas_row += 1
        y += 50
    tk.mainloop()
