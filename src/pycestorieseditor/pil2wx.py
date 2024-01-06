from __future__ import annotations

import wx
from PIL import Image, ImageDraw


def hex2rgb(color: str):
    c = color.lstrip("#")
    return tuple(int(c[i : i + 2], 16) for i in (0, 2, 4))


def create_icon(color=None):
    if not color:
        color = "#2ecc71"
    img = Image.new('RGBA', (16, 16))
    draw = ImageDraw.Draw(img)
    draw.rectangle(((1, 1), (14, 14)), fill=color, outline="black")
    return img


def pil_create_x():
    img = Image.new('RGBA', (16, 16))
    draw = ImageDraw.Draw(img)
    draw.ellipse((1, 1, 15, 15), fill="#ECECEC", outline="#8C8C8C")
    draw.line((4, 4, 11, 11), width=2, fill="black")
    draw.line((12, 4, 4, 12), fill="black")
    return img


def default_background():
    matrice = zip([x * 8 * 10 for x in range(1, 22)], [x * 4 * 10 for x in range(1, 22)])
    img = Image.new('RGBA', (445, 805))
    draw = ImageDraw.Draw(img)

    draw.rectangle(((0, 0), (445, 805)), fill="#ECECEC")

    for x, y in matrice:
        draw.line([(-10, x), (y, -10)], fill="#8C8C8C", width=10)

    draw.rectangle(((0, 0), (444, 804)), fill=None, outline="black")
    return wximage2bitmap(pil2wximage(img))


def pil2wximage(img: Image.Image):
    """Convert a PIL image to wxImage"""
    wx_image = wx.Image(*img.size)
    wx_image.SetData(img.convert('RGB').tobytes())
    wx_image.InitAlpha()
    alpha = img.getchannel("A").tobytes()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            wx_image.SetAlpha(i, j, alpha[i + j * img.size[0]])
    return wx_image


def wximage2bitmap(img):
    return img.ConvertToBitmap()


def wxicon(color=None):
    return wximage2bitmap(pil2wximage(create_icon(color)))


def wxcloseicon():
    return wximage2bitmap(pil2wximage(pil_create_x()))
