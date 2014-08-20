from flask.ext.login import login_required, current_user

from flask import render_template, redirect, url_for, flash, current_app, request, session, make_response

from .forms import CreateEventForm
from . import events
from .. import db
from ..models import User, Event
from ..decorators import admin_required

from datetime import timedelta
from datetime import datetime

@events.route('/', methods=['GET', 'POST'])
def events_list():
	page = request.args.get('page', 1, type=int)
	pagination = Event.query.order_by(Event.date.desc()).paginate(
		page, per_page=10,
		error_out=False)
	events = pagination.items
	return render_template('events/events_list.html', events=events, pagination=pagination)

@events.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_event():
	form = CreateEventForm()
	if form.validate_on_submit():
		event = Event(name=form.name.data,
					  code=form.code.data,
					  date=form.date.data)
		db.session.add(event)
		db.session.commit()
		flash('Your event has been created. Have users text %s to attend.' % event.code)
		return redirect(url_for('main.index'))
	return render_template('events/create.html', form=form)

@events.route('/register', methods=['GET', 'POST'])
def register():
	import twilio.twiml
	resp = twilio.twiml.Response()

	messagecount = int(session.get('count',0))

	response = make_response(str(resp))
	expires=datetime.utcnow() + timedelta(hours=3)
	response.set_cookie('count', value=str(messagecount),expires=expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))

	# check if we've interacted with this user recently
	if messagecount == 0: 
		shortcode = request.args['Body']
		session['shortcode'] = shortcode
		event = Event.query.filter_by(code=shortcode).first()
		session['event'] = event
		if event is None:
			resp.message('Sorry, we couldn\'t find an event with that shortcode.')
			return str(resp)
		resp.message('Hey there. Welcome to Michigan Hackers! Send your uniqname to register for this event.')
	elif messagecount == 1:
		uniqname = request.args['Body']

		# check if we 'know' this user
		user = User.query.filter_by(uniqname=uniqname).first()
		if user is None:
			session['newmember'] = True
			resp.message('Welcome to your first MH event! A few quick questions (we\'ll only ask you these once). What year are you? Reply with freshman, sophomore, junior, senior, graduate, or other.')
			# create new user with this uniqname and add them to our database
			user = User(email=uniqname + "@umich.edu",
						username=uniqname,
						uniqname=uniqname,
						password="password")
		else:
			resp.message('Thanks for registering, ' + uniqname)

		user.events.add(session['event'])
		db.session.add(user)
		db.session.commit()
	elif messagecount == 2 and session['newmember']:
		# eventually add this to some sort of spreadsheet for stats
		year = request.args['Body']
		resp.message('How\'d you hear about Michigan Hackers? Email or Facebook? If something else, respond with that.')
	elif messagecount == 3 and session['newmember']:
		# eventually add this to some sort of spreadsheet for stats
		reason_for_joining = request.args['Body']
		resp.message('Great! Would you like to be added to our member email list? Respond "YES" or "NO". If you\'re already on it, you can respond "NO".')
	elif messagecount == 4 and session['newmember']:
		add_to_email = request.args['Body']
		if add_to_email == "YES":
			#add to email list
			print 'hey'
		resp.message('Thanks so much for coming to our event. We hope to see you in the future!')

	# update message count and return twiml response	
	messagecount += 1
	session['count'] = str(messagecount)
	return str(resp)

