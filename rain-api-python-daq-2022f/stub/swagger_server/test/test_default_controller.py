# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.annual_rain_falls import AnnualRainFalls  # noqa: E501
from swagger_server.models.basin_full import BasinFull  # noqa: E501
from swagger_server.models.basin_short import BasinShort  # noqa: E501
from swagger_server.models.station_full import StationFull  # noqa: E501
from swagger_server.models.station_short import StationShort  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_controller_get_annual_rainfall(self):
        """Test case for controller_get_annual_rainfall

        Returns a total rainfalls on the speficied basin during the specified year.
        """
        response = self.client.open(
            '/basins/{basinId}/annualRainfalls/{year}'.format(basin_id=56, year=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_basin_details(self):
        """Test case for controller_get_basin_details

        Returns complete details of the specified basin
        """
        response = self.client.open(
            '/basins/{basinId}'.format(basin_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_basins(self):
        """Test case for controller_get_basins

        Returns a list of basins.
        """
        response = self.client.open(
            '/basins',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_station_details(self):
        """Test case for controller_get_station_details

        Returns complete details of the specified station
        """
        response = self.client.open(
            '/stations/{stationId}'.format(station_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_stations(self):
        """Test case for controller_get_stations

        Returns a list of stations located within the specified basin.
        """
        response = self.client.open(
            '/basins/{basinId}/stations'.format(basin_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
