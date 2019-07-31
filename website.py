from flask import Flask, render_template, redirect, url_for, session, flash, Markup
from urllib.parse import quote_plus
from flask_basicauth import BasicAuth

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

import post_test, new_email, os, smtplib


class HopecamForm(FlaskForm):
    username = StringField('Your Name', validators=[DataRequired()])
    apricot_username = StringField('Apricot Username', validators=[DataRequired()])
    apricot_password = PasswordField('Apricot Password', validators=[DataRequired()])
    outlook_username = StringField('Outlook Username', validators=[DataRequired()])
    outlook_password = PasswordField('Outlook Password', validators=[DataRequired()])
    submit = SubmitField('Get Started')


class SendEmailForm(FlaskForm):
    submit = SubmitField('Send Email')


app = Flask(__name__, static_url_path='', static_folder='')

app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)
# default auth values
app.config['BASIC_AUTH_USERNAME'] = os.getenv("BASIC_AUTH_USERNAME") or 'hopecam'
app.config['BASIC_AUTH_PASSWORD'] = os.getenv("BASIC_AUTH_PASSWORD") or 'hopecam'
# default value during development
app.secret_key = os.getenv("SECRET_KEY") or 'dev'

basic_auth = BasicAuth(app)


def get_first_item(list):
    if list:
        return list[0]


@app.route('/hopecam', methods=['GET', 'POST'])
@basic_auth.required
def hopecam_form():
    form = HopecamForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['apricot_username'] = form.apricot_username.data
        session['apricot_password'] = form.apricot_password.data
        session['outlook_username'] = form.outlook_username.data
        session['outlook_password'] = form.outlook_password.data
        return redirect(url_for('send_email_form'))
    return render_template('hopecam.html', title='Hopecam Form', form=form)


@app.route('/send_email_form', methods=['GET', 'POST'])
@basic_auth.required
def send_email_form():
    username = session.get('username')
    apricot_username = session.get('apricot_username')
    apricot_password = session.get('apricot_password')
    form = SendEmailForm()
    try:
        list_of_emails, requests_session, child_name_for_email_subject = \
            post_test.generate_email_params(username, apricot_username, apricot_password)
    except KeyError as ke:
        return render_template('send_email_content.html', to_email="No emails left", message="", form=form)
    except IndexError as ie:
        flash('There was a problem with your name or apricot credentials, please check your entries and try again.')
        return redirect(url_for('hopecam_form'))
    email_address = get_first_item(list_of_emails)[0]
    email_message = get_first_item(list_of_emails)[1]

    if form.validate_on_submit():
        outlook_username = session.get('outlook_username')
        outlook_password = session.get('outlook_password')
        try:
            new_email.send_email(outlook_username, outlook_password, email_address, email_message,
                                 child_name_for_email_subject)
        except smtplib.SMTPRecipientsRefused as sr:
            flash("No Email Receipients! Please update the Child's School Information")
            return render_template('send_email_content.html', to_email=email_address,
                                   message=email_message.split('\n'), form=form)
        except smtplib.SMTPException as se:
            flash(Markup('There was a problem with your email, please check your credentials back at <a href="' +
                         url_for('hopecam_form') + '" class="alert-link">/hopecam</a>'))
            return render_template('send_email_content.html', to_email=email_address,
                                   message=email_message.split('\n'), form=form)
        flash('Email sent!')
        new_email.update_connection_status(requests_session, username)
        return redirect(url_for('send_email_form'))

    return render_template('send_email_content.html', to_email=email_address,
                           message=email_message.split('\n'), form=form)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/blogs")
def blogs():
    return render_template('blogs.html')


if __name__ == "__main__":
    app.run()
