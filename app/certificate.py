# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from config import Config
from textwrap import fill
import qrcode
import os


def cert(form):
    temp_dir = 'app/static/temp'
    try:
        os.mkdir(temp_dir)
    except OSError as e:
        print(e)
    img = Image.open('app/template.png')
    idraw = ImageDraw.Draw(img)
    MAX_W, MAX_H = img.size
    text = f"{form.first_name} {form.last_name}"
    blank = Image.new('RGB', (1900, 500))
    fontsize = 100
    font = ImageFont.truetype(f"app/font/Shelley_Volante.ttf", size=fontsize)
    while (font.getsize(text)[0] < blank.size[0]) and (font.getsize(text)[1] < blank.size[1]):
        fontsize += 1
        font = ImageFont.truetype(f"app/font/Shelley_Volante.ttf", size=fontsize)
    w, h = idraw.textsize(text, font=font)
    x = (MAX_W - w) / 2
    y = (MAX_H - h) / 2
    idraw.text((x, y + 170), text, (49, 52, 76), font=font, align="center")
    text = fill(f"Имеет право владения планетой {form.name_cosmic}", 45)
    font = ImageFont.truetype(f"app/font/Shelley_Volante.ttf", size=100)
    w, h = idraw.textsize(text, font=font)
    x = (MAX_W - w) / 2
    y = (MAX_H - h) / 2
    idraw.text((x, y + 450), text, (76, 78, 82), font=font, align="center")
    font = ImageFont.truetype(f"app/font/SOUVENIR_NORMAL_0.TTF", size=50)
    text = form.datetime.strftime('%Y/%m/%d')
    w, h = idraw.textsize(text, font=font)
    x = (MAX_W - w) / 2
    y = (MAX_H - h) / 2
    idraw.text((x - 500, y + 1350), text, (122, 151, 128), font=font, align="center")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{Config.DOMAIN}cosmicBody_{form.cosmic_id}')
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white")
    (width, height) = img.size
    (width2, height2) = qr_code.size
    water_widht = width - width2 - 280
    water_height = height - height2 - 285
    img.paste(qr_code, (water_widht, water_height))
    img.save(f'{temp_dir}/{form.cosmic_id}.png', quality=100)
    return f'static/temp/{form.cosmic_id}.png'
