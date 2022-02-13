# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, send_file, safe_join, send_from_directory, url_for, abort, request
from app.forms import cosmic_print, cosmic_download
from app.certificate import cert
from config import Config
from app.models import *
from app import app
import datetime


USERS_AUTH = {}
START_TIME_AUTH = []
START_TIME_AUTH.append(datetime.datetime.now())
TIME_SESSION = 60 #Время активной сессии юзера
MAX_R = 20


@app.before_request
def hook():
    time_auth = START_TIME_AUTH[0]
    difference = datetime.datetime.now() - time_auth
    if difference.seconds >= TIME_SESSION:
        USERS_AUTH.clear()
        START_TIME_AUTH[0] = datetime.datetime.now()
    if USERS_AUTH.get(request.headers.get('User-Agent')):
        USERS_AUTH.get(request.headers.get('User-Agent'))[1] += 1
        if USERS_AUTH.get(request.headers.get('User-Agent'))[1] >= MAX_R:
            return "503", 503
        #print(USERS_AUTH.get(request.headers.get('User-Agent')))
    else:
        data = []
        data.append(datetime.datetime.now())
        data.append(0)
        USERS_AUTH.update({request.headers.get('User-Agent'): data})

@app.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
    return send_file(safe_join(f'static/favicon.png'))


#@app.route('/')
#@app.route('/index')
#def index():
#    return 'COSMICS'


@app.route('/cosm', methods=['GET', 'POST'])
def cosm():
    form = cosmic_print()
    if form.validate_on_submit():
        try:
            db.session.add(cosmic(first_name=form.first_name.data, last_name=form.last_name.data, name_cosmic=form.name_cosmic.data))
        except:
            db.session.add(cosmic(first_name=form.first_name.data, last_name=form.last_name.data, name_cosmic=form.name_cosmic.data))
        db.session.commit()
        form = db.session.query(cosmic).filter(cosmic.first_name == (form.first_name.data) and cosmic.last_name == (form.last_name.data) and cosmic.name_cosmic == (form.name_cosmic.data)).all()[-1]
        return redirect(f"{Config.DOMAIN}cosmicBody_{form.cosmic_id}")
        return f'<a href="{f"{Config.DOMAIN}cosmicBody_{form.cosmic_id}"}">{Config.DOMAIN}cosmicBody_{form.cosmic_id}</a>'
    return render_template('registration.html', form=form)


@app.route('/cosmicBody_<cosmic_id>', methods=['GET', 'POST'])
def cosmic_body(cosmic_id):
    if db.session.query(cosmic).filter(cosmic.cosmic_id == (cosmic_id)).all():
        form = db.session.query(cosmic).filter(cosmic.cosmic_id == (cosmic_id)).all()[0]
        if cosmic_download().validate_on_submit():
            try:
                return send_file(safe_join(f'static/temp/{form.cosmic_id}.png'), as_attachment=True)
            except:
                return send_file(cert(form), as_attachment=True)
        return render_template('certificate.html', form=form, cosmic_download=cosmic_download(),
                               title="Страница сертификата")
    else:
        abort(404)


@app.errorhandler(404)
def not_found_error(error):
    return send_file('static/404.jpg'), 404