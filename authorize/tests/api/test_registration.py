from rest_framework import status

from libs.api.test_mixins import BaseOEEAPITestCase, NotImplementedMixin


class RegistrationAPITestCase(
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
        self.base_url = '/auth/registration/'
        self.unimplemented_methods = ['get', 'put', 'patch', 'delete']
        self.anonymous_allowed_methods = ['post']
        self.mixins_test_obj_url = False
        self.mixins_test_list_url = True

        self.registration_data = {
            "username": "CBarbarian",
            "email": "support@open-energy-engine.org",
            "password1": "conansbutt",
            "password2": "conansbutt"
        }

        # This creates instance variable that are expected by tests and mixins
        super().setUp()

    def test_valid_registration_created(self):
        """
        Successful registration with valid data.
        """
        response = self.client_anon.post(
            self.base_url,
            data=self.registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_email_bad_request(self):
        """
        Bad request for improperly formatted email.
        """
        registration_data = self.registration_data
        registration_data["email"] = "invalid_email"

        response = self.client_anon.post(
            self.base_url,
            data=registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email_bad_request(self):
        """
        Bad request for missing email.
        """
        registration_data = self.registration_data
        registration_data.pop("email")

        response = self.client_anon.post(
            self.base_url,
            data=registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email_bad_request(self):
        """
        Bad request for registering pre-existing email address.
        """
        registration_data = self.registration_data
        registration_data["email"] = "storn+johnsnow@open-energy-engine.org"

        response = self.client_anon.post(
            self.base_url,
            data=registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username_bad_request(self):
        """
        Bad request for registering pre-existing username.
        """
        registration_data = self.registration_data
        registration_data["username"] = "johnsnow"

        response = self.client_anon.post(
            self.base_url,
            data=registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_username_bad_request(self):
        """
        Bad request for missing username.
        """
        registration_data = self.registration_data
        registration_data.pop("username")

        response = self.client_anon.post(
            self.base_url,
            data=registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unmatched_passwords_bad_request(self):
        """
        Bad request for registering with passwords that don't match.
        """
        registration_data = self.registration_data
        registration_data["password1"] = "winteriscoming"

        response = self.client_anon.post(
            self.base_url,
            data=registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_minimum_password_bad_request(self):
        """
        Bad request for 7 charector password.
        """
        registration_data = self.registration_data
        registration_data["password1"] = "1234567"
        registration_data["password2"] = "1234567"

        response = self.client_anon.post(
            self.base_url,
            data=registration_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
