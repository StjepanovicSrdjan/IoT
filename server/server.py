import datetime
import threading
from time import sleep

from flask import Flask, jsonify, request, render_template
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

with open('./settings.json') as json_file:
    config = json.load(json_file)

# InfluxDB Configuration
token = "H52k0xw1_YLEQW0KrfjVmEP6LknDslgnypqUpucnLoBUG7vW2XPdM9UIPsvtI4auGTAEJwm4hsTrle-DMeKzSA=="
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)
last_alarm_reset = datetime.datetime.utcnow()
alarm_state = False
CODE = [1, 2, 3, 4]
last_digits = []
security = False

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def on_connect(client, userdata, flags, rc):
    client.subscribe("DB")
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("DL")
    client.subscribe("UDS")
    client.subscribe("DMS")
    client.subscribe("DS_LEN")
    client.subscribe("PIR")
    client.subscribe("Gyroscope")
    print("Connected to MQTT broker")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


def check_password(data):
    global last_alarm_reset, alarm_state, last_digits, security
    if data["measurement"] == "DMS":
        last_digits.append(data["value"])
        last_digits = last_digits[-4:]
        print('Comparing code: ', last_digits, ' with ', CODE)
        if last_digits == CODE:
            last_alarm_reset = datetime.datetime.utcnow()
            alarm_state = False
            save_alarm_to_db("Correct code entered", False)
            security = not security


def save_to_db(data):
    check_password(data)
    print("Saving to DB")
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("measurement", data["value"])
    )
    print(point.to_line_protocol())
    write_api.write(bucket=bucket, org=org, record=point)


def save_alarm_to_db(reason, alarm_on=True):
    print("Saving alarm to DB")
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point('ALARM')
            .field("measurement", alarm_on)
    )
    print(point.to_line_protocol())
    write_api.write(bucket=bucket, org=org, record=point)
    point = (
        Point('ALARM_REASON')
            .tag("alarm_on", alarm_on)
            .field("measurement", reason)
    )
    print(point.to_line_protocol())
    write_api.write(bucket=bucket, org=org, record=point)


GET_LAST_DATA = """
from(bucket: "example_db")
  |> range(start: -1h)
  |> tail(n: 1)
"""
DS_LEN_MAX = """
from(bucket: "example_db")
  |> range(start: %sZ)
  |> filter(fn: (r) => r._measurement == "DS_LEN")
  |> max()
"""


def handle_influx_query(query):
    query_api = influxdb_client.query_api()
    tables = query_api.query(query, org=org)

    container = []
    for table in tables:
        for record in table.records:
            container.append(record.values)

    return jsonify({"status": "success", "data": container})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', devices_config=config)


@app.route('/api/last', methods=['GET'])
def get_last():
    return handle_influx_query(GET_LAST_DATA)


@app.route('/api/drop/<measurement>', methods=['GET'])
def drop_measurement(measurement):
    query_api = influxdb_client.delete_api()
    query_api.delete(
        "1970-01-01T00:00:00Z", datetime.datetime.now(),
        f'_measurement="{measurement}"',
        bucket=bucket, org=org
    )
    return jsonify({"status": "success"})


def check_ds():
    global alarm_state, last_alarm_reset
    query_api = influxdb_client.query_api()
    print(DS_LEN_MAX % last_alarm_reset.isoformat())
    tables = query_api.query(DS_LEN_MAX % last_alarm_reset.isoformat(), org=org)
    for table in tables:
        for record in table.records:
            print(record.values)
            if record.values["_value"] > 5.0:
                print("ALARM")
                alarm_state = True
                save_alarm_to_db(f"Door ({record.values['name']}) stuck for {record.values['_value']} s", True)


def check_alarms():
    global alarm_state, last_alarm_reset
    while True:
        if not alarm_state:
            try:
                check_ds()
            except Exception as e:
                print(e)
        sleep(2)


ds_thread = threading.Thread(
    target=check_alarms
)

if __name__ == '__main__':
    app.run(debug=True)
    ds_thread.start()
