import mysql.connector
from datetime import datetime, timedelta

db = mysql.connector.connect(
  host="iot.cpe.ku.ac.th",
  user="b6310545426",
  password="siratee.k@ku.th",
  database="b6310545426"
)

def fetch_data_from_db(mysql: mysql.connector.MySQLConnection, table: str) -> list:
    cursor = mysql.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

def insert_into_db(mysql: mysql.connector.MySQLConnection, data: list):
    cursor = mysql.cursor(dictionary=True)
    for i in data:
        query = "INSERT INTO weather (ts, lat, lon, sensor, source, value) VALUE ("
        query += "'%s'," % i["ts"].strftime("%Y-%m-%d %H:%M:%S")
        query += "%s," % i["lat"]
        query += "%s," % i["lon"]
        query += "'%s'," % i["sensor"]
        query += "'%s'," % i["source"]
        query += "%s" % i["value"]
        query += ")"
        print(query)
        cursor.execute(query)
    mysql.commit()
    return

def cal_avg_data(data: list[dict], field: str) -> float:
    sum_data = sum([x.get(field, 0) for x in data])
    return sum_data / len(data)

def cal_sum_data(data: list[dict], field: str) -> float:
    return sum([x.get(field, 0) for x in data])

def normalize_data(data: list, value_function, sensor: str, source: str) -> list:
    result = []
    for i in range(0, len(data)-1):
        focused_data = data[i]
        value = value_function(focused_data)
        lat =focused_data["lat"]
        lon  =focused_data["lon"]
        try:
            latest_timestamp = focused_data["timestamp"]
        except:
            latest_timestamp = focused_data["ts"]
        result.append({
            "ts": latest_timestamp,
            "lat": lat,
            "lon": lon,
            "sensor": sensor,
            "source": source,
            "value": value,
        })
    return result

# Get Data from each table
aqi_data = fetch_data_from_db(db, "aqi")
kid_bright_data = fetch_data_from_db(db, "kidbright")
tmd_data = fetch_data_from_db(db, "tmd")

result = normalize_data(aqi_data,lambda data: data["pm25"], "pm25", "aqi")
result = result + normalize_data(kid_bright_data, lambda data: data["light"], "light", "kidbright")
result = result + normalize_data(kid_bright_data,lambda data: data["temp"], "temperature", "kidbright")
result = result + normalize_data(tmd_data,lambda data: data["humidity"], "humidity", "tmd")
result = result + normalize_data(tmd_data,lambda data: data["temperature"], "temperature", "tmd")
result = result + normalize_data(tmd_data,lambda data: data["rainfall"], "rain", "tmd")

# Sort data by date
result.sort(key=lambda value: value["ts"], reverse=True)

result_groupped = []

# # Insert into db
current_time_range = datetime(2022, 10, 21, 0, 0, 0)
while len(result) != 0:
    data = []
    while len(result) != 0:
        focused_data = result.pop(-1)
        if focused_data["ts"] > current_time_range:
            result.append(focused_data)
            break
        data.append(focused_data)

    if len(data) != 0:
        sensors = {}
        for i in data:
            if i["source"] not in sensors:
                sensors[i["source"]] = {
                    i["sensor"]: [i]
                }
                continue
            
            if i["sensor"] not in sensors[i["source"]]:
                sensors[i["source"]][i["sensor"]] = [i]
                continue

            sensors[i["source"]][i["sensor"]].append(i)

        for source in sensors:
            for sensor in sensors[source]:
                result_groupped.append({
                            "ts": current_time_range,
                            "lat": cal_avg_data(sensors[source][sensor], "lat"),
                            "lon": cal_avg_data(sensors[source][sensor], "lon"),
                            "sensor": sensor,
                            "source": source,
                            "value": cal_sum_data(sensors[source][sensor], "value") if sensor == "rain" else  cal_avg_data(sensors[source][sensor], "value"),
                        })
    current_time_range = current_time_range + timedelta(hours=6)
insert_into_db(db, result_groupped)
