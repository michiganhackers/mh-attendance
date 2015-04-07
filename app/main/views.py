from flask.ext.login import login_required, current_user

from flask import render_template, current_app, redirect, url_for, flash, g

from .forms import CreateUserInfoForm, CreateCodeEnterForm
from ..models import User, Event
from .. import db
from . import main

import gspread
import os

@main.route('/', methods=['GET', 'POST'])
def index():
	infoForm = CreateUserInfoForm();
	codeForm = CreateCodeEnterForm();
	print g.get('_gspread')

	if infoForm.validate_on_submit():
		email = infoForm.email.data
		techtalks = infoForm.mc_tech_talks.data
		core = infoForm.mc_core.data
		
		# check if we 'know' this user
		# user = User.query.filter_by(email=email).first()
		# if user is None:
			# uniqname = email.split("@")[0]
			# create new user with this uniqname and add them to our database
			# user = User(email=uniqname + "@umich.edu",
			# 			username=uniqname,
			# 			uniqname=uniqname,
			# 			attend_talks=techtalks,
			# 			join_core=core,
			# 			password="password")
			# db.session.add(user)
			# db.session.commit()
		gc = gspread.Client(auth=(os.environ.get('GMAIL'), os.environ.get('GMAIL_PWD')))
		gc.login()
		sheet = gc.open_by_key(os.environ.get('SPREADSHEET_KEY')).sheet1
		num_rows = len(sheet.col_values(1))
		sheet.append_row([email, techtalks, core])
		# sheet.update_acell('A' + str(num_rows + 1), email)
			# print "Added user %s to the database." % email

			# Add the email to google spreadsheet (and uniqname to Twilio backend?)
		flash("You've been subscribed to the Michigan Hackers E-mail list. We send out E-mails every Wednesday so be on the lookout!", 'success')
		return redirect(url_for('main.index'))

	if codeForm.validate_on_submit():
		shortcode = codeForm.code.data

		event = Event.query.filter_by(code=shortcode).first()
		if event is None:
			flash('Sorry, we couldn\'t find an event with that shortcode.')
			return redirect(url_for('main.index'))
		else:
			return redirect(url_for('events.web_register', event=event))

	return render_template('index.html', infoForm=infoForm, codeForm=codeForm)