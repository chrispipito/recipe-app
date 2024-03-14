import unittest
from app import create_app


class RecipeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client(use_cookies=True)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_recipes_page(self):
        response = self.client.get('/recipes')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
