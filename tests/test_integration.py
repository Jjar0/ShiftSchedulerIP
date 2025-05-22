import unittest
from shiftapp import app, db
from shiftapp.models import User

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            user = User(username='admin', password='admin', role='admin')
            db.session.add(user)
            db.session.commit()

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_invalid_login(self):
        response = self.app.post('/login', data=dict(username='wrong', password='user'), follow_redirects=True)
        self.assertIn(b'Invalid credentials', response.data)

    def test_valid_login_redirects(self):
        self.app.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
        response = self.app.get('/admin', follow_redirects=True)
        self.assertIn(b'Admin Dashboard', response.data)

    def tearDown(self):
        with app.app_context():
            db.drop_all()
