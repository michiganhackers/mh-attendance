from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User


class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64),
											 Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Log In')

class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64),
											 Email()])
	username = StringField('Username', validators=[
		Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
										  'Usernames must have only letters, '
										  'numbers, dots or underscores')])
	uniqname = StringField('Uniqname', validators=[Required(), Length(1, 64)])
	password = PasswordField('Password', validators=[
		Required(), EqualTo('password2', message='Make those passwords match!')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Sign up')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Username is already in use.')

	def validate_uniqname(self, field):
		user = User.query.filter_by(uniqname=field.data).first()
		if user and user.username is not None:
			raise ValidationError('We already have a username associated with that uniqname.')

class ChangePasswordForm(Form):
	old_password = PasswordField('Old password', validators=[Required()])
	password = PasswordField('New password', validators=[
		Required(), EqualTo('password2', message='Make those passwords match!')])
	password2 = PasswordField('Confirm your new password', validators=[Required()])
	submit = SubmitField('Update Password')

class PasswordResetRequestForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64),
											 Email()])
	submit = SubmitField('Reset password')

class PasswordResetForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64),
											 Email()])
 	password = PasswordField('New Password', validators=[Required(),
					EqualTo('password2', message='Make those passwords match!')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Reset Password')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('Unknown email address.')

class ChangeEmailForm(Form):
	email = StringField('New Email', validators=[Required(), Length(1, 64),
												 Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Update email address')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email has already been registered.')

