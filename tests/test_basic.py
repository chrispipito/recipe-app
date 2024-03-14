import unittest
from app import create_app


class HomePageTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
