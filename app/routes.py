# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, send_file, safe_join, send_from_directory, url_for, abort
from app import app
import json
from app.models import *
from app.forms import cosmic_print, cosmic_download
from datetime import timezone
from PIL import Image, ImageDraw, ImageFont
from slugify import slugify
import os
import shutil
from textwrap import fill

@app.route('/')
@app.route('/index')
def index():
    return 'Hello, world'


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
                shutil.rmtree(temp_dir)
            except OSError as e:
                print(e)
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
            img.save(f'{temp_dir}/{form.cosmic_id}.png', quality=100)
            return send_file(safe_join(f'static/temp/{form.cosmic_id}.png'))
            return redirect(url_for('good'))
            return send_file(safe_join(f'static/temp/{form.cosmic_id}.pdf'), as_attachment=True)
        return render_template('certificate.html', form=form, cosmic_download=cosmic_download(), title="Страница сертификата")
    else:
        abort(404)


@app.errorhandler(404)
def not_found_error(error):
    return send_file('static/404.jpg'), 404