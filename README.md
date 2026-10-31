# ming-stack

Local IoT stack for an ESP32 + DHT22 sensor: **Mosquitto** (MQTT) → **Node-RED** → **InfluxDB** → **Grafana**.

## Quick start

```sh
cp .env.example .env   # then edit the passwords and token
docker compose up -d
```

| Service   | URL / Port              |
|-----------|-------------------------|
| Node-RED  | http://localhost:1880   |
| Grafana   | http://localhost:3000   |
| InfluxDB  | http://localhost:8086   |
| Mosquitto | `localhost:1883` (MQTT) |

## Find your computer's IP

The ESP32 connects to the broker over your LAN, so set `MQTT_BROKER` in `dht_code/config.py` to your computer's IP.

- **macOS:** `ipconfig getifaddr en0` (try `en1` if empty)
- **Windows:** `ipconfig` and look for the IPv4 Address of your Wi-Fi adapter

## Folders

- `dht_code/` – MicroPython code for the ESP32. Set your Wi-Fi and MQTT details in `config.py`.
- `nodered/` – Node-RED flows and settings.
- `provisioning/` – Config files that are committed to git and mounted into containers (read-only) so a fresh clone works without manual setup. For example, `mosquitto.conf` configures the broker. This is kept separate from the runtime volumes (`influxdb/`, `grafana/`, `mosquitto/data/`), which hold generated data and are git-ignored.
