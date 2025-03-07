#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import NamedTuple


class Size(NamedTuple):
    width: int = 0
    height: int = 0


IMAGE = Size(45, 80)
BORDER = Size(2, 2)
ROW_HEIGHT = IMAGE.height + 2 * BORDER.height
TEXT_WIDTH = 200                # 10 pix / char

