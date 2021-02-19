from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.contrib.auth.models import User


class BaseOEEAPITestCase(APITestCase):
    """
    Update this.  Scale it back.
    """
    fixtures = [
        'users.json'
    ]

    # Override these:
    base_url = ''       # e.g. /v1/user/
    unimplemented_methods = []
    anonymous_allowed_methods = []
    mixins_test_obj_url = True
    mixins_test_list_url = True

    # Set this this in setUp():
    base_queryset = None

    # Optional, if present will test the extended case only!
    url_extension = ''  # e.g. register/ in /v1/user/161/register/

    def setUp(self):
        """
        Sets the base_queryset and resets starting conditions before
        the execution of each test.

        Subclasses must define a base_queryset in this method *before*
        calling super().setUp!!!
        """
        self.USER_PASSWORD = 'winteriscoming'

        # Active user
        self.user_auth = User.objects.get(pk=1)

        # Inactive user
        self.user_unauth = User.objects.get(pk=2)

        # Create clients.
        # Anonymous client
        self.client_anon = APIClient()

        # Authorized client.
        self.client_auth = APIClient()
        response = self.client_auth.post(
            '/auth/login/',
            {
                'username': self.user_auth.username,
                'password': self.USER_PASSWORD
            }
        )
        self.client_auth.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data.get('key')
        )

        # Unauthorized client.
        self.user_unauth.is_active = True   # Will reset to False shortly
        self.user_unauth.save()
        self.client_unauth = APIClient()
        response = self.client_unauth.post(
            '/auth/login/',
            {
                'username': self.user_unauth.username,
                'password': self.USER_PASSWORD
            }
        )
        self.client_unauth.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data.get('key')
        )
        self.user_unauth.is_active = False
        self.user_unauth.save()

        # Get common testing stuff.
        if self.base_queryset:
            self.obj = self.base_queryset.first()
            self.obj_url = '%s%i/%s' % (
                self.base_url, self.obj.id, self.url_extension)
            self.obj_data = vars(self.obj)
            self.obj_data.pop('_state')
        else:
            self.obj = None

        self.list_url = '%s%s' % (self.base_url, self.url_extension)

        self.unimplemented_methods = \
            [method.lower() for method in self.unimplemented_methods]

        self.unauthenticated_code = status.HTTP_401_UNAUTHORIZED

        self.anonymous_allowed_methods = \
            [method.lower() for method in self.anonymous_allowed_methods]


class NotImplementedMixin(object):
    """
    Mixes standard tests into BaseOEEAPITestCase for checking that
    users receive a 504 response for unimplemented methods.
    """

    def test_not_implemented(self):
        """
        Test that authorized users get 405 responses for all unimplemented
        methods at all regular object and list endpoints.
        """
        data = {}

        # Get
        if 'get' in self.unimplemented_methods:
            if self.mixins_test_obj_url:
                response = self.client_auth.patch(self.obj_url)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            if self.mixins_test_list_url:
                response = self.client_auth.patch(self.list_url)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Post
        if 'post' in self.unimplemented_methods:
            if self.mixins_test_list_url:
                response = self.client_auth.post(self.list_url, data)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Put
        if 'put' in self.unimplemented_methods:
            if self.mixins_test_obj_url:
                response = self.client_auth.put(self.obj_url, data)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Patch
        if 'patch' in self.unimplemented_methods:
            if self.mixins_test_obj_url:
                response = self.client_auth.patch(self.obj_url, data)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            if self.mixins_test_list_url:
                response = self.client_auth.patch(self.list_url, data)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Delete
        if 'delete' in self.unimplemented_methods:
            if self.mixins_test_obj_url:
                response = self.client_auth.delete(self.obj_url)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
            if self.mixins_test_list_url:
                response = self.client_auth.delete(self.list_url)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
