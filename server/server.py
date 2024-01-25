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
alarm_door_stuck = False
CODE = [1, 2, 3, 4]
last_digits = []
security_mode = False
alarm_security = False
alarm_gyro = False

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
    global last_alarm_reset, alarm_door_stuck, last_digits, security_mode, alarm_security
    if data["measurement"] == "DMS":
        last_digits.append(data["value"])
        last_digits = last_digits[-4:]
        if last_digits == CODE:
            last_alarm_reset = datetime.datetime.utcnow()
            alarm_door_stuck = False
            alarm_security = False
            alarm_gyro = False
            save_alarm_to_db("Correct code entered", False)
            security_mode = not security_mode


def check_security(data):
    global last_alarm_reset, security_mode, alarm_security

    if security_mode and not alarm_security:
        if data["measurement"] == "DS_LEN":
            alarm_security = True
            save_alarm_to_db(f"Somebody opened door ({data['name']}) while security was ON", True)


def check_gyro(data):
    global last_alarm_reset, alarm_gyro

    if data["measurement"] == "Gyroscope":
        alarm_gyro = True
        save_alarm_to_db(f"Sufficient movement detected ({data['name']}) - maybe earthquake", True)


def save_to_db(data):
    check_password(data)
    check_security(data)
    check_gyro(data)

    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


def save_alarm_to_db(reason, alarm_on=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point('ALARM')
            .field("measurement", alarm_on)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    point = (
        Point('ALARM_REASON')
            .tag("alarm_on", alarm_on)
            .field("measurement", reason)
    )
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


@app.route('/api/alarm', methods=['GET'])
def get_alarm():
    return jsonify({"status": "success", "alarm": alarm_door_stuck or alarm_security or alarm_gyro})


@app.route('/api/alarm/off', methods=['POST'])
def alarm_off():
    global alarm_door_stuck, alarm_security, alarm_gyro, last_alarm_reset
    alarm_door_stuck = False
    alarm_security = False
    alarm_gyro = False
    last_alarm_reset = datetime.datetime.utcnow()
    save_alarm_to_db("Alarm turned off via website", False)
    return jsonify({"status": "success"})


def check_ds():
    global alarm_door_stuck, last_alarm_reset
    query_api = influxdb_client.query_api()
    tables = query_api.query(DS_LEN_MAX % last_alarm_reset.isoformat(), org=org)
    for table in tables:
        for record in table.records:
            if record.values["_value"] > 5.0:
                alarm_door_stuck = True
                save_alarm_to_db(f"Door ({record.values['name']}) stuck for {record.values['_value']} s", True)


def check_alarms():
    global alarm_door_stuck, last_alarm_reset
    while True:
        if not alarm_door_stuck:
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
