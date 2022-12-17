import sys
from flask import abort
import pymysql as mysql
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

sys.path.append(OPENAPI_STUB_DIR)
from swagger_server import models

db = mysql.connect(host=DB_HOST,
                   user=DB_USER,
                   passwd=DB_PASSWD,
                   db=DB_NAME)


def get_basins():
    with db.cursor() as cs:
        cs.execute("SELECT basin_id,ename FROM basin")
        result = [models.BasinShort(basin_id, name) for basin_id, name in cs.fetchall()]
    return result

def get_basin_details(basin_id):
    with db.cursor() as cs:
        cs.execute("""
            SELECT basin_id, ename, area
            FROM basin
            WHERE basin_id=%s
            """, [basin_id])
        result = cs.fetchone()
    if result:
        basin_id, name, area = result
        return models.BasinFull(basin_id, name, area)
    else:
        abort(404)


def get_stations(basin_id):
    with db.cursor() as cs:
        cs.execute("""
            SELECT station_id, s.ename
            FROM station s
            INNER JOIN basin b ON s.basin_id=b.basin_id
            WHERE b.basin_id=%s
            """, [basin_id])
        result = [models.StationShort(station_id, name) for station_id, name in cs.fetchall()]
    return result

def get_annual_rainfall(basin_id, year):
    with db.cursor() as cs:
        cs.execute("""
            SELECT SUM(daily_amount)
            FROM (
                SELECT year, month, day, AVG(amount) as daily_amount FROM rainfall r
                INNER JOIN station s ON s.station_id=r.station_id
                INNER JOIN basin b ON s.basin_id=b.basin_id
                WHERE b.basin_id=%s AND year=%s
                GROUP BY year, month, day
            ) daily_amount
        """, [basin_id, year])
    result = cs.fetchone()
    if result and len(result) == 1:
        return models.AnnualRainFalls(basin_id, year, result[0])
    abort(404)

def get_station_details(station_id):
    with db.cursor() as cs:
        cs.execute("""
            SELECT station_id, basin_id, ename, lat, lon
            FROM station
            WHERE station_id=%s
        """, [station_id])
        result = cs.fetchone()
    if result:
        station_id, basin_id, name, lat, lon = result
        return models.StationFull(station_id, basin_id, name, lat, lon)
    abort(404)

