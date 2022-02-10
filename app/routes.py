# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, send_file, safe_join, send_from_directory, url_for, abort, request
import qrcode
from app import app
from app.models import *
from app.forms import cosmic_print, cosmic_download
from PIL import Image, ImageDraw, ImageFont
from slugify import slugify
import os
from textwrap import fill
from config import Config

@app.route('/good')
def good():
    return 'Форму принял!'


@app.route('/call', methods=['GET', 'POST'])
def call():
    form = cosmic_print()
    if form.validate_on_submit():
        db.session.add(cosmic(first_name=form.first_name.data, last_name=form.last_name.data, name_cosmic=form.name_cosmic.data))
        db.session.commit()
        return redirect('/good')
    return render_template('call.html', form=form)

@app.route('/cosmicBody_<cosmic_id>', methods=['GET', 'POST'])
def cosmic_body(cosmic_id):
    if db.session.query(cosmic).filter(cosmic.cosmic_id == (cosmic_id)).all() != []:
        form = db.session.query(cosmic).filter(cosmic.cosmic_id == (cosmic_id)).all()[0]
        if cosmic_download().validate_on_submit():
            temp_dir = 'app/static/temp'
            try:
                os.mkdir(temp_dir)
            except OSError as e:
                print(e)
            img = Image.open('app/template.png')
            font = ImageFont.truetype(f"app/font/DISTANT_STROKE_MEDIUM.OTF", size=350)
            idraw = ImageDraw.Draw(img)
            MAX_W, MAX_H = img.size
            text = f"{slugify(form.first_name)} {slugify(form.last_name)}"
            w, h = idraw.textsize(text, font=font)
            x = (MAX_W - w) / 2
            y = (MAX_H - h) / 2
            idraw.text((x, y + 170), text, (49, 52, 76), font=font, align="center")
            text = fill(f"This certificate confirms that a {slugify(form.first_name)} {slugify(form.last_name)} has the right to own planet {slugify(form.name_cosmic)}", 70)
            font = ImageFont.truetype(f"app/font/DISTANT_STROKE.OTF", size=120)
            w, h = idraw.textsize(text, font=font)
            x = (MAX_W - w) / 2
            y = (MAX_H - h) / 2
            idraw.text((x, y + 450), text, (76, 78, 82), font=font, align="center")
            font = ImageFont.truetype(f"app/font/SOUVENIR_NORMAL_0.TTF", size=50)
            text = form.datetime.strftime('%Y/%m/%d')
            w, h = idraw.textsize(text, font=font)
            x = (MAX_W - w) / 2
            y = (MAX_H - h) / 2
            idraw.text((x-500, y + 1350), text, (122, 151, 128), font=font, align="center")
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f'{Config.DOMAIN}cosmicBody_{cosmic_id}')
            qr.make(fit=True)
            qr_code = qr.make_image(fill_color="black", back_color="white")
            qr_code.save("some_file.png")
            (width, height) = img.size
            (width2, height2) = qr_code.size
            water_widht = width - width2 - 280
            water_height = height - height2 - 285
            img.paste(qr_code, (water_widht, water_height))
            img.save(f'{temp_dir}/{form.cosmic_id}.png', quality=100)
            #return send_file(safe_join(f'static/temp/{form.cosmic_id}.png'))
            return send_file(safe_join(f'static/temp/{form.cosmic_id}.png'), as_attachment=True)
        return render_template('certificate.html', form=form, cosmic_download=cosmic_download(), title="Страница сертификата")
    else:
        abort(404)


@app.errorhandler(404)
def not_found_error(error):
    return send_file('static/404.jpg'), 404