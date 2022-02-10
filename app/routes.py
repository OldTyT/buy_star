# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, send_file, safe_join, send_from_directory
from app import app
import json
from app.models import *
from app.forms import cosmic_print, cosmic_download
from datetime import timezone
import pdfkit
import os
import shutil

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
        pdf_form = cosmic_download()
        if pdf_form.validate_on_submit():
            temp_dir = 'app/static/temp'
            try:
                shutil.rmtree(temp_dir)
            except OSError as e:
                print(e)
            try:
                os.mkdir(temp_dir)
            except OSError as e:
                print(e)
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
            }
            pdfkit.from_string(render_template('certificate.html', form=form, cosmic_download=pdf_form), f'{temp_dir}/{form.cosmic_id}.pdf', options=options, css="app/static/certificate.css")
            #pdfkit.from_url(f'http://172.28.95.149:8888/cosmicBody_{form.cosmic_id}', f'{temp_dir}/{form.cosmic_id}.pdf')
            return send_file(safe_join(f'static/temp/{form.cosmic_id}.pdf'), as_attachment=True)
        return render_template('certificate.html', form=form, cosmic_download=pdf_form)
    else:
        return "404"