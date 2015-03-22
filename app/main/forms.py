from flask.ext.wtf import Form
from wtforms import StringField, DateTimeField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email
from wtforms import ValidationError

class CreateUserInfoForm(Form):
	email = StringField('', validators=[Required(), Length(1, 64), Email()])
	mc_tech_talks = BooleanField('I would like to attend technical talks with Michigan Hackers.')
	mc_core = BooleanField('I want to join the Michigan Hackers Core group to be a more involved member.')
	submit = SubmitField('Subscribe')

class CreateCodeEnterForm(Form):
	code = StringField('', validators=[Required(), Length(1,64)])
	submit = SubmitField('Go')
