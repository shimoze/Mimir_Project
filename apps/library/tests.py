from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book
from django.urls import reverse

# Create your tests here.

class BookModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            year=2023,
            content='Some content',
            owner=self.user
        )

    def test_book_string_representation(self):
        self.assertEqual(str(self.book), 'Test Book')

    def test_book_content(self):
        self.assertEqual(self.book.author, 'Test Author')

    def test_book_year_is_2023(self):
        self.assertEqual(self.book.year, 2023)

class BookViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password')

    def test_home_page_status_code(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_book_redirect_anonymous(self):

        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login', response.url)

    def test_create_book_logged_in(self):
        self.client.login(username='tester', password= 'password')

        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')

