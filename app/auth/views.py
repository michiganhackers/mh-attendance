from . import auth
from .. import db
from ..models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		return
	return render_template('auth/register.html', form=form)