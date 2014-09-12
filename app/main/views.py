from flask.ext.login import login_required, current_user

from flask import render_template, current_app, redirect, url_for, flash, g

from .forms import CreateUserInfoForm
from ..models import User
from .. import db
from . import main

import gspread
import os

@main.route('/', methods=['GET', 'POST'])
def index():
	form = CreateUserInfoForm();
	print g.get('_gspread')

	if form.validate_on_submit():
		email = form.email.data
		techtalks = form.mc_tech_talks.data
		core = form.mc_core.data
		
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
	return render_template('index.html', form=form)