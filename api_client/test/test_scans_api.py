# coding: utf-8

"""
    Super Linter

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from linter_api_client.api.scans_api import ScansApi


class TestScansApi(unittest.TestCase):
    """ScansApi unit test stubs"""

    def setUp(self) -> None:
        self.api = ScansApi()

    def tearDown(self) -> None:
        pass

    def test__scans_get(self) -> None:
        """Test case for _scans_get

        Read Scans
        """
        pass

    def test__scans_post(self) -> None:
        """Test case for _scans_post

        Create Scan
        """
        pass

    def test__scans_project_id_start_post(self) -> None:
        """Test case for _scans_project_id_start_post

        Start Scan
        """
        pass

    def test__scans_project_project_id_get(self) -> None:
        """Test case for _scans_project_project_id_get

        Read Project Scans
        """
        pass

    def test__scans_scan_id_get(self) -> None:
        """Test case for _scans_scan_id_get

        Read Scan
        """
        pass


if __name__ == '__main__':
    unittest.main()
