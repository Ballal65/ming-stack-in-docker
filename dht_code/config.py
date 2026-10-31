# WiFi credentials
WIFI_SSID     = "<YOUR_WIFI_SSID>"
WIFI_PASSWORD = "<YOUR_WIFI_PASSWORD>"

MQTT_BROKER = "192.168.1.9"   # your Mac's LAN IP (found via `ifconfig`, interface en1)
MQTT_PORT   = 1883

# MQTT auth (mosquitto now requires this -- see mosquitto/config/mosquitto.conf)
MQTT_USERNAME = "dht22device"
MQTT_PASSWORD = "changeme123"

# A unique name for this device on the broker
MQTT_CLIENT_ID = "esp32_dht22"

# Topics this device publishes to
TOPIC_TEMPERATURE = b"home/dht22/temperature"
TOPIC_HUMIDITY     = b"home/dht22/humidity"
TOPIC_LED_TOGGLE = b"home/dht22/led-toggle"
TOPIC_LED_STATUS = b"home/dht22/led-status"

# Pins
DHT_PIN   = 21
LED_PIN   = 2    # onboard LED -> WiFi connection indicator
LED2_PIN  = 17   # extra LED   -> controlled remotely via MQTT