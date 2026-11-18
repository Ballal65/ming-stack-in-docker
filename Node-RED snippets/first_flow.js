if (msg.topic.endsWith("temperature")) {
    msg.payload = { temperature: parseFloat(msg.payload) };
} else if (msg.topic.endsWith("humidity")) {
    msg.payload = { humidity: parseFloat(msg.payload) };
} else if (msg.topic.endsWith("led-status")) {
    msg.payload = { led: parseInt(msg.payload) };
} else {
    return null; // ignore status, led-toggle and other control topics
}
return msg;