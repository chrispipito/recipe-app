import unittest
from app import app, db
from models import Recipe


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            recipe = Recipe(name='Test Recipe #1', ingredients='Test Ingredients', instructions='Test Instructions')
            db.session.add(recipe)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the Recipe App', response.data.decode())

    def test_add_recipe_form(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add a New Recipe', response.data.decode())

    def test_recipe_submission(self):
        # Simulate form data for a new recipe
        form_data = {
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'instructions': 'Some cooking instructions'
        }

        # Simulate POST request to submit the form
        response = self.client.post('/add', data=form_data, follow_redirects=True)

        # Verify that the submission was successful
        self.assertEqual(response.status_code, 200)

        # Using app context to query the database
        with app.app_context():
            added_recipe = Recipe.query.filter_by(name='Test Recipe').first()

        # Assertions to verify the recipe was correctly added
        self.assertIsNotNone(added_recipe)
        self.assertEqual(added_recipe.ingredients, 'Ingredient 1, Ingredient 2')
        self.assertEqual(added_recipe.instructions, 'Some cooking instructions')

    def test_view_recipes(self):
        with app.app_context():
            db.session.add(Recipe(name='Test Recipe', ingredients='Ingredient', instructions='instructions'))
            db.session.commit()
        response = self.client.get('/recipes')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Recipe', response.data.decode())

    def test_view_recipe_details(self):
        with app.app_context():
            recipe = Recipe(name='Sample Recipe', ingredients='ingredients', instructions='instructions')
            db.session.add(recipe)
            db.session.commit()
            recipe_id = recipe.id
        response = self.client.get(f'/recipes/{recipe_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Recipe', response.data.decode())
        self.assertIn('Ingredients', response.data.decode())
        self.assertIn('Instructions', response.data.decode())

    def test_get_all_recipes_with_api(self):
        response = self.client.get('api/recipes')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn('recipes', data)

        recipes = data['recipes']
        self.assertIsInstance(recipes, list)

        self.assertGreater(len(recipes), 0)
        self.assertIn('name', recipes[0])
        self.assertIn('ingredients', recipes[0])
        self.assertIn('instructions',recipes[0])
        self.assertEqual(recipes[0]['name'], 'Test Recipe #1')


if __name__ == '__main__':
    unittest.main()
