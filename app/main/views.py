from flask.ext.login import login_required, current_user

from flask import render_template, current_app

from . import main

@main.route('/', methods=['GET'])
def index():
	from twilio.rest import TwilioRestClient

	client = TwilioRestClient(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])
 
	message = client.messages.create(body="Go Blue!",
	    to=current_app.config['TWILIO_TEST_SEND_TO_NUMBER'],    # Replace with your phone number
	    from_=current_app.config['TWILIO_FROM_NUMBER']) # Replace with your Twilio number
	print message.sid
	return render_template('index.html')