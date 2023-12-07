from flask import url_for
from flask_login import current_user, login_user

from application.auth.models import User
from .base import BaseTest

class AuthTest(BaseTest):
    
    def test_view_register(self):
        '''Tests if the register page loads correctly.'''
        with self.client:
            response = self.client.get(url_for('auth.register'))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'register', response.data)
            self.assertIn(b'Username', response.data)
            self.assertIn(b'Sign up', response.data)
            
    def test_register_post(self):
        '''Tests if user registration works successfully.'''
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(username='test', email='test@test.com', password='password', confirm_password='password'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account successfully created', response.data)
        user = User.query.filter_by(email='test@test.com').first()
        self.assertIsNotNone(user)
    
    def test_view_login(self):
        '''Tests if the login page loads correctly.'''
        with self.client:
            response = self.client.get(url_for('auth.login'))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Password', response.data)
            self.assertIn(b'Remember me', response.data)
            self.assertIn(b'Login', response.data)
            
    def test_login(self):
        '''Tests if user login works successfully.'''
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data=dict(email='user@gmail.com', password='password'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have been logged in successfully!', response.data)
            self.assertTrue(current_user.is_authenticated)
            
    def test_logout(self):
        '''Tests if user logout works successfully.'''
        login_user(User.query.filter_by(id=1).first())
            
        response = self.client.post(url_for('auth.logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out successfully', response.data)
        self.assertFalse(current_user.is_authenticated)

    def test_update(self):
        '''Tests if user account update works successfully.'''
        login_user(User.query.filter_by(id=1).first())

        with self.client:
            response = self.client.post(
                url_for('auth.account'),
                data=dict(username='updated', email='user@gmail.com', about_me="hello"),
                follow_redirects=True
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your account has been updated', response.data)

            self.assertEqual(current_user.username, 'updated')
            self.assertEqual(current_user.about_me, 'hello')
        
    
    