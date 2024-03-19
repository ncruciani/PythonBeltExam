from flask import render_template, redirect, request, session
from flask import flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    user = User.get_by_id({'id': session['user_id']})
    cars = Car.get_all()
    return render_template("dashboard.html", user=user, cars=cars)


@app.route("/cars/new")
def new_car():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    return render_template("new_car.html")


@app.route("/cars/new/process", methods=["POST"])
def create_car():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    errors = Car.validate_car(data)
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect("/cars/new")
    id = Car.save(data)
    session['car_id'] = id
    flash("car successfully created!", "success")
    return redirect("/dashboard")


@app.route("/cars/<int:car_id>")
def view_car(car_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    car = Car.get_by_id({'id': car_id})
    if not car:
        flash("car not found.", "error")
        return redirect("/dashboard")
    return render_template("view.html", car=car)


@app.route("/cars/edit/<int:car_id>")
def edit_car(car_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    car = Car.get_by_id({'id': car_id})
    if not car:
        flash("Car not found.", "error")
        return redirect("/dashboard")
    if car.creator.id != session['user_id']:
        flash("You are not authorized to edit this car.", "error")
        return redirect("/dashboard")
    return render_template("edit_car.html", car=car)



@app.route("/cars/edit/process/<int:car_id>", methods=["POST"])
def update_car(car_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    car = Car.get_by_id({'id': car_id})
    if not car:
        flash("Car not found.", "error")
        return redirect("/dashboard")
    if car.creator.id != session['user_id']:
        flash("You are not authorized to edit this car.", "error")
        return redirect("/dashboard")
    form_data = {
        'id': car.id,
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description']
    }
    errors = Car.validate_car(request.form)
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(f"/cars/edit/{car.id}")
    
    Car.update(form_data)
    flash("Car successfully updated!", "success")
    return redirect("/dashboard")


@app.route("/cars/purchase/<int:car_id>")
def purchase_car(car_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    car = Car.get_by_id({'id': car_id})
    if not car:
        flash("Car not found.", "error")
        return redirect("/dashboard")
    Car.delete({'id': car_id})
    flash("Car successfully deleted!", "success")
    return redirect("/dashboard")

@app.route("/cars/destroy/<int:car_id>")
def delete_car(car_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    car = Car.get_by_id({'id': car_id})
    if not car:
        flash("Car not found.", "error")
        return redirect("/dashboard")
    if car.creator.id != session['user_id']:
        flash("You are not authorized to delete this car.", "error")
        return redirect("/dashboard")
    Car.delete({'id': car.id})
    flash("Car successfully deleted!", "success")
    return redirect("/dashboard")
