import unittest
from flask_testing import TestCase
from app import create_app


class TestBase(TestCase):
    def create_app(self):
        app = create_app()
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///:memory:', TESTING=True)
        return app


class TestHome(TestBase):
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Recipe App', response.data)


if __name__ == '__main__':
    unittest.main()
