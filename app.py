from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define your Recipe model here, or import it if defined in models.py

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add', methods=['GET'])
def add_recipe_form():
    return render_template('add_recipe.html')


# Add other routes here

if __name__ == '__main__':
    app.run(debug=True)
