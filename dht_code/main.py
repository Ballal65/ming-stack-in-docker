import network
import time
from machine import Pin
import dht
from umqttsimple import MQTTClient
import config

# ── Setup ───────────────────────────────────────────────────────────────────
wifi_led = Pin(config.LED_PIN, Pin.OUT)    
cmd_led = Pin(config.LED2_PIN, Pin.OUT) 
sensor = dht.DHT22(Pin(config.DHT_PIN))
LED_status = False

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    try:
        sta_if.config(pm=network.WLAN.PM_NONE)
    except (AttributeError, ValueError):
        pass

    if not sta_if.isconnected():
        print(f"Connecting to WiFi '{config.WIFI_SSID}'...")
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            wifi_led.value(not wifi_led.value())
            time.sleep(0.3)
    wifi_led.value(1)
    print("WiFi connected, IP:", sta_if.ifconfig()[0])
    time.sleep(1)

def on_mqtt_message(topic, msg):
    global LED_status
    print("Command received:", topic, msg)
    if topic == config.TOPIC_LED_TOGGLE:
        if msg.strip().lower() == b"on":
            cmd_led.value(1)
            LED_status = True
        elif msg.strip().lower() == b"off":
            cmd_led.value(0)
            LED_status = False
        else:
            print("Unrecognized LED command:", msg)
            
def connect_mqtt():
    client = MQTTClient(
        config.MQTT_CLIENT_ID,
        config.MQTT_BROKER,
        port=config.MQTT_PORT,
        user=config.MQTT_USERNAME,
        password=config.MQTT_PASSWORD,
        keepalive=60,
    )
    client.set_callback(on_mqtt_message)
    client.connect()
    client.subscribe(config.TOPIC_LED_TOGGLE)
    print(f"Connected to MQTT broker at {config.MQTT_BROKER}:{config.MQTT_PORT}")
    print(f"Subscribed to {config.TOPIC_LED_TOGGLE}")
    return client


# ── Main ────────────────────────────────────────────────────────────────────

connect_wifi()
mqtt = connect_mqtt()

while True:
    try:
        # Check for any incoming LED comman
        mqtt.check_msg()

        # DHT22 requires a sampling delay of at least 0.5 seconds between readings
        time.sleep(0.5)

        # Trigger a new measurement
        sensor.measure()

        # Retrieve temperature and humidity values
        temp = sensor.temperature()  # Celsius
        hum = sensor.humidity()      # relative humidity %

        print(f"Temperature: {temp:.1f}C  Humidity: {hum:.1f}% LED status {LED_status}")

        # Publish each reading as its own small message
        mqtt.publish(config.TOPIC_TEMPERATURE, str(round(temp,2)).encode())
        mqtt.publish(config.TOPIC_HUMIDITY, str(round(hum,2)).encode())
        mqtt.publish(config.TOPIC_LED_STATUS, str(int(LED_status)).encode())

    except OSError as e:
        print("Failed to read data from the DHT22 sensor.", e)

    except Exception as e:
        # MQTT connection dropped
        print("MQTT error, reconnecting...", e)
        try:
            mqtt = connect_mqtt()
        except Exception as e2:
            print("Reconnect failed:", e2)
            time.sleep(2)

