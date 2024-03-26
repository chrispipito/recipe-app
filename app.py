# app.py
from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models import Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add', methods=['GET'])
def add_recipe_form():
    return render_template('add_recipe.html')


@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        # Create a new Recipe instance
        new_recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions)

        # Add to the database
        db.session.add(new_recipe)
        db.session.commit()

        # Redirect to home page after successful addition
        return redirect(url_for('home'))

    # If not a POST request, just render the form
    return render_template('add_recipe.html')


@app.route('/recipes')
def view_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)


@app.route('/api')
def hello_api():
    return {'message': 'Hello, API!'}


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    recipes_data = []
    for recipe in recipes:
        recipes_data.append({
            'id': recipe.id,
            'name': recipe.name,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions
        })
    return {'recipes': recipes_data}


if __name__ == '__main__':
    app.run(debug=True)
