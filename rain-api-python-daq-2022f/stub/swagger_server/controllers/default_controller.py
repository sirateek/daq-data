import connexion
import six

from swagger_server.models.annual_rain_falls import AnnualRainFalls  # noqa: E501
from swagger_server.models.basin_full import BasinFull  # noqa: E501
from swagger_server.models.basin_short import BasinShort  # noqa: E501
from swagger_server.models.station_full import StationFull  # noqa: E501
from swagger_server.models.station_short import StationShort  # noqa: E501
from swagger_server import util


def controller_get_annual_rainfall(basin_id, year):  # noqa: E501
    """Returns a total rainfalls on the speficied basin during the specified year.

     # noqa: E501

    :param basin_id: 
    :type basin_id: int
    :param year: 
    :type year: int

    :rtype: AnnualRainFalls
    """
    return 'do some magic!'


def controller_get_basin_details(basin_id):  # noqa: E501
    """Returns complete details of the specified basin

     # noqa: E501

    :param basin_id: 
    :type basin_id: int

    :rtype: BasinFull
    """
    return 'do some magic!'


def controller_get_basins():  # noqa: E501
    """Returns a list of basins.

     # noqa: E501


    :rtype: List[BasinShort]
    """
    return 'do some magic!'


def controller_get_station_details(station_id):  # noqa: E501
    """Returns complete details of the specified station

     # noqa: E501

    :param station_id: 
    :type station_id: int

    :rtype: StationFull
    """
    return 'do some magic!'


def controller_get_stations(basin_id):  # noqa: E501
    """Returns a list of stations located within the specified basin.

     # noqa: E501

    :param basin_id: 
    :type basin_id: int

    :rtype: List[StationShort]
    """
    return 'do some magic!'
