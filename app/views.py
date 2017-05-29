from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/index')
def index():
    users = [
                {"name":"Soren", "number":"123456"},
                {"name":"Soren2", "number":"987654"}
             ]
    return render_template('index.html', users = users, )
