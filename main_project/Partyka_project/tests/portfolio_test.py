from flask import url_for
from .base import BaseTest

class PortfolioTest(BaseTest):
    def test_view_index(self):
        '''Tests if the portfolio index page loads correctly.'''
        with self.client:
            response = self.client.get(url_for('portfolio.home'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome!', response.data)

    def test_view_about(self):
        '''Tests if the portfolio about page loads correctly.'''
        with self.client:
            response = self.client.get(url_for('portfolio.page1'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Eddie', response.data)

    def test_view_skills(self):
        '''Tests if the portfolio skills page loads correctly.'''
        with self.client:
            response = self.client.get(url_for('portfolio.skills'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Python', response.data)
            self.assertIn(b'HTML', response.data)