# coding: utf-8

"""
    Super Linter

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from linter_api_client.api.users_api import UsersApi


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self) -> None:
        self.api = UsersApi()

    def tearDown(self) -> None:
        pass

    def test__users_get(self) -> None:
        """Test case for _users_get

        Read Users
        """
        pass

    def test__users_post(self) -> None:
        """Test case for _users_post

        Create User
        """
        pass

    def test__users_user_id_get(self) -> None:
        """Test case for _users_user_id_get

        Read User
        """
        pass


if __name__ == '__main__':
    unittest.main()
