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
        self.base_url = '/auth/logout/'
        self.unimplemented_methods = ['get', 'put', 'patch', 'delete']
        self.anonymous_allowed_methods = ['post']
        self.mixins_test_obj_url = False
        self.mixins_test_list_url = True

        # This creates instance variable that are expected by tests and mixins
        super().setUp()

    def test_logout_okay(self):
        """
        Successful logout by posting to endpoint.
        :return:
        """
        response = self.client_auth.post(
            self.base_url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
