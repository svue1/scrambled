# @author: Aberdeen Morrow
# Last Modified: 12-02-21
# Macalester College
# COMP 446 Internet Computing
# with Joslenne Pena

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import json

# load recipe data
fake_recipes_json=open('static/fake_recipes.json')
recipe_data = json.load(fake_recipes_json)

#creating app instance of flask
app = Flask(__name__)
#defining sql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#need a secret key for user session authentication
app.config['SECRET_KEY'] = 'thisissecret'

#initialize the database
db = SQLAlchemy(app)
#create a required loginmanager class and object
login_manager = LoginManager()
#configure application object for login
login_manager.init_app(app)

#create a user class acting as db model for users table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String())

db.create_all()

#callback is used to reload the user object from the 
# user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    title = "Scrambled"
    return render_template("home.html", title=title, logged_in=current_user.is_authenticated) # can set any different variables

@app.route("/recipes")
def recipes():
    return render_template("recipes.html", 
                            title="Recipes",
                            all_recipes=recipe_data,
                            logged_in=current_user.is_authenticated)

@app.route('/recipe')
def recipe():
    return render_template("recipe.html", 
                            title="Recipe",
                            logged_in=current_user.is_authenticated)
# @app.route("/recipe/<id>")
# def recipe(id):
#     return render_template("recipe.html", title=recipe['name'], recipe=recipe)
    # return render_template("recipe.html", title=db.query.get(id).title, recipe=db.query.get(id))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        if request.form.get('action') == 'Sign Up':
            username = request.form['username']
            # Ensures username is unique
            if User.query.filter_by(username=username).count() > 0:
                alert = 'Username \'' + username + '\' is already in use. Please choose a different username.'
                flash(alert)
                return render_template('register.html', alert=alert)
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            # try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/')
        elif request.form.get('action') == 'Log In':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if check_password_hash(user.password, password):
                login_user(user)
                try:
                    next = request.form['next']
                    return redirect(next)
                except:
                    return redirect('/')
            else:
                flash('Username and password do not match. Please try again.')
                return redirect('/login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_term = request.form['search']
    # search_results = []
    # for recipe in recipe_data:
    #     for recipe['ingredients'] in recipe:
    #         if search_term == recipe['ingredients']['name']:
    #             search_results.append(recipe)
    return render_template("search.html", 
                            search_term=search_term, 
                            search_results=recipe_data,
                            logged_in=current_user.is_authenticated) #, title=""+search_term+"", search_term=search_term)

@app.route("/user")
@login_required
def profile():
    return render_template("profile.html", title="Your Recipes", logged_in=current_user.is_authenticated)

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return 'you are now logged out'

if __name__ == '__main__':
    app.run(debug=True)