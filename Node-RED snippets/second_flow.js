msg.topic = "home/dht22/led";
msg.payload = msg.payload.status === "firing" ? "ON" : "OFF";
return msg;