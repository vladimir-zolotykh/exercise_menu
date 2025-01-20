#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


def grid_expand(w):
    # Equivalent to:
    # w.rowconfigure(0, weight=1)
    # w.columnconfigure(0, weight=1)
    for meth in ['rowconfigure', 'columnconfigure']:
        getattr(w, meth)(0, weight=1)


class ScrolledCanvas(tk.Canvas):
    def __init__(self, owner, **kwargs):
        box = tk.Frame(owner)
        box.grid(column=0, row=0, sticky=tk.NSEW)
        grid_expand(box)
        hbar = tk.Scrollbar(box, orient=tk.HORIZONTAL, command=self.xview)
        hbar.grid(column=0, row=1, sticky=tk.EW)
        vbar = tk.Scrollbar(box, orient=tk.VERTICAL, command=self.yview)
        vbar.grid(column=1, row=0, sticky=tk.NS)
        kwargs.update({'xscrollcommand': hbar.set, 'yscrollcommand': vbar.set})
        super().__init__(box, **kwargs)
        self.grid(column=0, row=0, sticky=tk.NSEW)
        for meth in dir(box):
            attr = getattr(box, meth)
            if meth.startswith('grid') and callable(attr):
                setattr(self, meth, attr)
        
                      
