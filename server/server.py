from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json


app = Flask(__name__)


# InfluxDB Configuration
token = "H52k0xw1_YLEQW0KrfjVmEP6LknDslgnypqUpucnLoBUG7vW2XPdM9UIPsvtI4auGTAEJwm4hsTrle-DMeKzSA=="
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


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
    client.subscribe("DS")
    client.subscribe("PIR")
    print("Connected to MQTT broker")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


def save_to_db(data):
    print("Saving to DB")
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
