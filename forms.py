from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


## Contact form
class ContactForm(FlaskForm):
    full_name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = TextAreaField("Your Message", validators=[DataRequired()])
    send = SubmitField("Send Message")


## Login form
class LoginForm(FlaskForm):
    email = StringField()
    password = PasswordField("Password")
    login = SubmitField("Log In")
    

## Register form
class RegisterForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8)])
    register = SubmitField("Register")
    

## Shipping form
class ShippingForm(FlaskForm):
    firstname = StringField("First Name (Required)", validators=[DataRequired()])
    lastname = StringField("Last Name (Required)", validators=[DataRequired()])
    email = StringField("Email (Required)", validators=[DataRequired()])
    phone = StringField("Phone Number (Optional)", )
    addressline1 = StringField("Address Line 1 (Required)", validators=[DataRequired()])
    addressline2 = StringField("Address Line 2 (Optional)")
    city = StringField("City (Required)", validators=[DataRequired()])
    state = StringField("State (Required)", validators=[DataRequired()])
    zipcode = StringField("Zipcode (Required)", validators=[DataRequired()])
    back = SubmitField("Back to Cart")
    proceed = SubmitField("Proceed to Payment")
    

## Quantity selection
class OrderQuantity(FlaskForm):
    quantity_dropdown = SelectField("Order Quantity", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], validators=[DataRequired()])
    addtocart = SubmitField("Add to Cart")