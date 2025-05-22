import unittest
from shiftapp import app, db
from shiftapp.models import User, Shift

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        # set test config
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF for test client
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # use in-memory db
        self.client = app.test_client()

        # set up app context and database
        with app.app_context():
            db.create_all()
            # add admin user for testing login
            admin = User(username='admin', password='admin', role='admin')
            db.session.add(admin)
            db.session.commit()

    # test login page returns 200 OK and contains login heading
    def test_login_page_loads(self):  # ID: 5
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    # test invalid login displays flash message
    def test_invalid_login(self):  # ID: 6
        response = self.client.post('/login', data=dict(username='wrong', password='user'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)

    # test successful login redirects to admin dashboard
    def test_valid_login_redirects(self):  # ID: 7
        response = self.client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)

    def tearDown(self):
        # teardown database and app context
        with app.app_context():
            db.session.remove()
            db.drop_all()
