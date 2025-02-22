from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, DateField, TextAreaField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

# Login Form
class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    remember = BooleanField('Remember me')  
    submit = SubmitField('Log In')


# Registration Form
class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    submit = SubmitField('Register')


# Trip Search Form
class TripSearchForm(FlaskForm):
    query = StringField('Search Destination', validators=[Optional()])
    min_price = DecimalField('Min Price', validators=[Optional()])
    max_price = DecimalField('Max Price', validators=[Optional()])
    start_date = DateField('Start Date', validators=[Optional()])
    submit = SubmitField('Search')


# Add Trip Form
class AddTripForm(FlaskForm):
    code = StringField(
        'Trip Code',
        validators=[
            DataRequired(message="Trip code is required."),
            Length(max=50, message="Trip code must be 50 characters or less.")
        ]
    )
    name = StringField(
        'Trip Name',
        validators=[
            DataRequired(message="Trip name is required."),
            Length(max=100, message="Trip name must be 100 characters or less.")
        ]
    )
    length = StringField(
        'Length (ex. 7 days)',
        validators=[
            DataRequired(message="Trip length is required.")
        ]
    )
    start = DateField(
        'Start Date',
        validators=[
            DataRequired(message="Start date is required.")
        ],
        format='%Y-%m-%d'
    )
    resort = StringField(
        'Resort Name',
        validators=[
            DataRequired(message="Resort name is required."),
            Length(max=100, message="Resort name must be 100 characters or less.")
        ]
    )
    per_person = FloatField(
        'Price Per Person',
        validators=[
            DataRequired(message="Price per person is required."),
            NumberRange(min=0.01, message="Price per person must be greater than zero.")
        ]
    )
    image = StringField(
        'Image Name',
        validators=[
            DataRequired(message="Image name is required."),
            Length(max=200, message="Image name must be 200 characters or less.")
        ]
    )
    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(message="Description is required.")
        ]
    )
    submit = SubmitField('Add Trip')


# Edit Trip Form
class EditTripForm(FlaskForm):
    code = StringField(
        'Trip Code',
        validators=[
            DataRequired(message="Trip code is required."),
            Length(max=50, message="Trip code must be 50 characters or less.")
        ]
    )
    name = StringField(
        'Trip Name',
        validators=[
            DataRequired(message="Trip name is required."),
            Length(max=100, message="Trip name must be 100 characters or less.")
        ]
    )
    length = StringField(
        'Length (ex. 7 days)',
        validators=[
            DataRequired(message="Trip length is required.")
        ]
    )
    start = DateField(
        'Start Date',
        validators=[
            DataRequired(message="Start date is required.")
        ],
        format='%Y-%m-%d'
    )
    resort = StringField(
        'Resort Name',
        validators=[
            DataRequired(message="Resort name is required."),
            Length(max=100, message="Resort name must be 100 characters or less.")
        ]
    )
    per_person = FloatField(
        'Price Per Person',
        validators=[
            DataRequired(message="Price per person is required."),
            NumberRange(min=0.01, message="Price per person must be greater than zero.")
        ]
    )
    image = StringField(
        'Image Name',
        validators=[
            DataRequired(message="Image name is required."),
            Length(max=200, message="Image name must be 200 characters or less.")
        ]
    )
    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(message="Description is required.")
        ]
    )
    submit = SubmitField('Update Trip')  
