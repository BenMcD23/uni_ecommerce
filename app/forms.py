import re
# so can query database
from app import models, current_user


from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


def email_validator(form, email):
    # checking valid email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
        raise ValidationError('Invalid Email')

    # checking if account with email exits
    if models.Accounts.query.filter_by(email=email.data).first():
        raise ValidationError('An account with this email already exists')


def password_validator(form, password):
    # checking got atleast 1 letter and 1 number
    if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]", password.data):
        raise ValidationError(
            'Password must contain at least 1 letter and 1 number')


def login_email_validator(form, email):
    # global user so can use it in the password validator
    global user

    # if there isnt an account with that email
    user = models.Accounts.query.filter_by(email=email.data).first()
    if not user:
        raise ValidationError('An account with this email doesnt exist')


def login_password_validator(form, password):
    # only if there is a user, avoids error
    if user:
        # if the password isnt the same as the one provided
        if user.password != password.data:
            raise ValidationError('Incorrect password')


def postcode_valiadator(form, postcode):
    # check if the postcode is valid
    if re.match(r"^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([AZa-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))[0-9][A-Za-z]{2})$", postcode.data):
        raise ValidationError('Postcode is not in the correct format, please ensure it is in the format XXXX XXX')


def changePass_password_validator(form, password):
    # compares the current logged in password to one provided
    if current_user.password != password.data:
        raise ValidationError('Incorrect password')


def tags_valiadtor(form, productTag):
    # if the tag isnt in the database
    if not models.Tags.query.filter_by(tagName=productTag.data).all():
        raise ValidationError('That tag does not exist')


# for signing up
class SignupForm(FlaskForm):
    firstName = TextField('firstName', validators=[DataRequired()])
    lastName = TextField('lastName', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired(), email_validator])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=25, message="Password must be between 6 and 25 characters"), password_validator])
    passwordValidate = PasswordField('passwordValidate', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])

    createAccount = SubmitField('Create Account')


# for logging in
class LoginForm(FlaskForm):
    email = TextField('email', validators=[DataRequired(), login_email_validator])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=25, message="Password must be between 6 and 25 characters"), login_password_validator])

    submitLogin = SubmitField('Login')


# for adding an address
class AddressForm(FlaskForm):
    houseNumName = TextField('houseNumName', validators=[DataRequired()])
    street = TextField('street', validators=[DataRequired()])
    town = TextField('town', validators=[DataRequired()])
    postcode = TextField('postcode', validators=[DataRequired(), postcode_valiadator])

    submitAddress = SubmitField('Add')


# for changing pass
class ChangePass(FlaskForm):
    currentPassword = PasswordField('currentPassword', validators=[DataRequired(), Length(min=6, max=25, message="Password must be between 6 and 25 characters"), changePass_password_validator])
    newPassword = PasswordField('newPassword', validators=[DataRequired(), Length(min=6, max=25, message="Password must be between 6 and 25 characters"), password_validator])
    newPasswordValidate = PasswordField('newPasswordValidate', validators=[DataRequired(), EqualTo('newPassword', message="Passwords must match")])

    submitPass = SubmitField('Submit')


# for searching products with tag
class SearchProductsForm(FlaskForm):
    productTag = TextField('productTag', validators=[Length(max=50, message="Tags cannot be over 50 characters"), tags_valiadtor])

    submitSearch = SubmitField('Search')
