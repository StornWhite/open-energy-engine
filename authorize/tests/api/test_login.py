from rest_framework import status

from libs.api.test_mixins import BaseOEEAPITestCase, NotImplementedMixin


class LoginAPITestCase(
    NotImplementedMixin,
    BaseOEEAPITestCase
):
    """
    Automated test suite for the login endpoint, which can accept POST
    requests from anonymous users containing either a username and password
    or email address and password.
    """
    def setUp(self):
        """
        Sets up users and endpoints before each of the set of tests.
        """
        # Customization overrides
        self.base_url = '/auth/login/'
        self.unimplemented_methods = ['get', 'put', 'patch', 'delete']
        self.anonymous_allowed_methods = ['post']
        self.mixins_test_obj_url = False
        self.mixins_test_list_url = True

        # This creates instance variable that are expected by tests and mixins
        super().setUp()

    def test_login_username_okay(self):
        """
        Successful login with working username/password.
        """
        login_data = {
            "username": "johnsnow",
            "password": "winteriscoming"
        }
        response = self.client_anon.post(
            self.base_url,
            data=login_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_email_okay(self):
        """
        Successful login with working email/password.
        """
        login_data = {
            "email": "storn+johnsnow@open-energy-engine.org",
            "password": "winteriscoming"
        }
        response = self.client_anon.post(
            self.base_url,
            data=login_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_username_bad_request(self):
        """
        Bad request if incorrect username.
        """
        login_data = {
            "username": "johnsnow,esquire",
            "password": "winteriscoming"
        }
        response = self.client_anon.post(
            self.base_url,
            data=login_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_email_bad_request(self):
        """
        Bad request if incorrect email.
        """
        login_data = {
            "email": "johnsnow@example.com",
            "password": "winteriscoming"
        }
        response = self.client_anon.post(
            self.base_url,
            data=login_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_password_bad_request(self):
        """
        Bad request if incorrect password
        """
        login_data = {
            "username": "johnsnow",
            "password": "summeristhebest!"
        }
        response = self.client_anon.post(
            self.base_url,
            data=login_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user_bad_request(self):
        """
        Bad request if user is inactive.
        """
        login_data = {
            "username": "robbstark",
            "password": "winteriscoming"
        }
        response = self.client_anon.post(
            self.base_url,
            data=login_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
