from tethys_sdk.testing import TethysTestCase
from ..app import MyFirstApp

from bs4 import BeautifulSoup


class HomeControllerTestCase(TethysTestCase):
    """
    Since the home controller has the @login_required decorator, it will behave differently depending on whether a user
    is or is not logged in. This class handles the testing of both cases.
    """

    def set_up(self):
        self.user = self.create_test_user(username="joe", email="joe@some_site.com", password="secret")
        self.c = self.get_test_client()

    def test_not_logged_in(self):
        # Without doing a login, the Client object, c, acts as an AnonymousUser
        response = self.c.get('/apps/my-first-app/')
        # Since the home controller has the @login_required decorator, if not logged in the page redirects, returning
        # a 302 status code in the initial response
        self.assertEqual(response.status_code, 302)

        # If the get request has the "follow" parameter set to True, the redirect will be followed, and should return
        # a 200 status code.
        response = self.c.get('/apps/my-first-app/', follow=True)

        # Check that the response returned successfully
        self.assertEqual(response.status_code, 200)

        # Check that the request was redirected only once to the login page
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertTrue('login' in response.redirect_chain[0][0])

    def test_logged_in(self):
        self.c.force_login(self.user)
        response = self.c.get('/apps/my-first-app/')
        self.assertEqual(response.status_code, 200)


class MapControllerTestCase(TethysTestCase):
    def set_up(self):
        self.create_test_persistent_stores_for_app(MyFirstApp)
        self.create_test_user(username="joe", email="joe@some_site.com", password="secret")
        self.c = self.get_test_client()

    def tear_down(self):
        self.destroy_test_persistent_stores_for_app(MyFirstApp)

    def test_context_and_html(self):
        # Can be tested without logging in since there is no @login_required decorator
        response = self.c.get('/apps/my-first-app/map/')

        # Check that the response returned successfully
        self.assertEqual(response.status_code, 200)

        # Check that the response returned the context variable
        self.assertIsNotNone(response.context['map_options'])

        # Check that the html was rendered correctly based on the context variable
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue('active' in soup.find(id='link-AllGages')['class'])
        self.assertTrue(len(soup.find(id='gizmo-map').contents) > 0)


class MapSingleControllerTestCase(TethysTestCase):
    def set_up(self):
        self.create_test_persistent_stores_for_app(MyFirstApp)
        self.create_test_user(username="joe", email="joe@some_site.com", password="secret")
        self.c = self.get_test_client()

    def tear_down(self):
        self.destroy_test_persistent_stores_for_app(MyFirstApp)

    def test_context_and_html(self):
        for i in range(1, 5):
            # Can be tested without logging in since there is no @login_required decorator
            response = self.c.get('/apps/my-first-app/map/{id}/'.format(id=i))

            # Check that the response returned successfully
            self.assertEqual(response.status_code, 200)

            # Check that the response returned the context variable
            self.assertIsNotNone(response.context['map_options'])
            self.assertEqual(int(response.context['gage_id']), i)

            # Check that the html was rendered correctly based on the context variable
            soup = BeautifulSoup(response.content, 'html.parser')
            html_gage_id = 'link-Gage{id}'.format(id=i)
            self.assertTrue('active' in soup.find(id=html_gage_id)['class'])
            self.assertTrue(len(soup.find(id='gizmo-map').contents) > 0)


class EchoNameControllerTestCase(TethysTestCase):
    def set_up(self):
        self.create_test_user(username="joe", email="joe@some_site.com", password="secret")
        self.c = self.get_test_client()

    def test_context_and_html(self):
        test_names = ['Jerry', 'Elaine', 'George', 'Kramer']

        for name in test_names:
            # Can be tested without logging in since there is no @login_required decorator
            response = self.c.post('/apps/my-first-app/echo-name/', {'name-input': name})

            # Check that the response returned successfully
            self.assertEqual(response.status_code, 200)

            # Check that the response returned the context variable
            self.assertIsNotNone(response.context['text_input_options'])
            self.assertEqual(response.context['name'], name)

            # Check that the html was rendered correctly based on the context variable
            soup = BeautifulSoup(response.content, 'html.parser')
            welcome_string = 'Hello, {name}!'.format(name=name)
            self.assertEqual(soup.find(id='h1-Greeting').string, welcome_string)
