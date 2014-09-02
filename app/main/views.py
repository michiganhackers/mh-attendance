from flask.ext.login import login_required, current_user

from flask import render_template, current_app, redirect, url_for, flash

from .forms import CreateUserInfoForm

from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
	form = CreateUserInfoForm();
	if form.validate_on_submit():
		email = form.email.data
		techtalks = form.mc_tech_talks.data
		core = form.mc_core.data
		# Do something witht he db here.
		# Add the email to google spreadsheet (and uniqname to Twilio backend?)
		flash("You've been subscribed to the Michigan Hackers E-mail list. We send out E-mails every Wednesday so bee on the lookout!", 'success')
		return redirect(url_for('main.index'))
	return render_template('index.html', form=form)