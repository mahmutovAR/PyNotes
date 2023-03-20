from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .views import homepage


class HomePageTest(TestCase):
    def test_homepage_one(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_homepage_two(self):
        request = HttpRequest()
        response = homepage(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startwith('<html>'))
        self.assertIn('<title>TITTLE NAME</title>', html)
        self.assertTrue(html.endswith('</html>'))
