from flask.ext.login import login_required, current_user

from flask import render_template

from . import main

@main.route('/', methods=['GET'])
def index():
	data = 'useless showing Han how do use Git'
	return render_template('index.html')