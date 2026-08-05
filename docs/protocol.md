# NexusChat Protocol

Version: 0.1

---

## Overview

The NexusChat Protocol defines the communication contract between clients and the NexusChat server.

Communication occurs over a WebSocket connection.

---

# WebSocket Endpoint

/ws

---

# Connection

Clients establish a WebSocket connection using:

```ws://<host>:<port>/ws```

Example
```
ws://localhost:8000/ws?username=Bharat
```

---

# Required Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | string | Yes | User's display name |

---

# Connection Validation

The server validates the handshake before accepting the connection.

Validation Rules

- username is required
- username cannot be empty

If validation fails

- Reject the WebSocket connection
- Log the reason

---

# Successful Connection

After validation, the server creates a ClientSession.

##### Example:
```

ClientSession

username = Bharat

websocket = <WebSocket>
```

---

# Message Format

(Current Version)

Messages are plain UTF-8 text.

##### Example:
```
Hello Everyone
```

---

# Broadcast Format

(Current Version)
```
<username>: <message>
```

##### Example:
```
Bharat: Hello Everyone
```

---

# Future Extensions

Planned

- Unique usernames
- Join notifications
- Leave notifications
- Private messaging
- Chat rooms
- JSON message protocol
- Authentication
- JWT