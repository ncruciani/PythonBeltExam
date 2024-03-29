from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/user/process', methods=['POST'])
def register_user():
    if not User.validate_user(request.form):
        flash('Please fix the form errors!', 'register')
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/main/page')



@app.route('/login/user', methods=['POST'])
def login_user():
    one_user = User.get_by_email(request.form)
    if not one_user:
        flash('account doesnt exist or wrong input for email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/')
    session['user_id'] = one_user.id
    return redirect('/main/page')


@app.route('/main/page')
def main_page():
    if 'user_id' not in session:
        flash('You need to log in first buddy', 'login/user')
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    one_user = User.get_by_id(data)
    cars = Car.get_all()
    flash_messages = get_flashed_messages(with_categories=True)
    return render_template('dashboard.html', user=one_user, cars=cars)


@app.route('/logout')
def logout():
    session.clear()
    flash('your now logged out good luck')
    return redirect('/')