# NexusChat Protocol

Version: 0.2

---

# Overview

The NexusChat Protocol defines the communication contract between clients and the NexusChat server.

Communication occurs over a WebSocket connection.

---

# WebSocket Endpoint
```
/ws
```
---

# Connection

Clients establish a WebSocket connection using:
```
ws://<host>:<port>/ws
```
#### Example
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

Validation occurs immediately after the WebSocket handshake.

Validation Rules

- username is required
- username cannot be empty
- username must be unique

If validation fails

- The server sends an error message to the client.
- The server closes the WebSocket connection.
- No ClientSession is created.
- The user is not added to the ConnectionManager.

#### Example

ERROR: Username 'Bharat' is already in use.

---

# Connection Lifecycle

Successful Connection
```
Client
    │
    ▼
WebSocket Handshake
    │
    ▼
Server accepts connection
    │
    ▼
Validation
    │
    ▼
ClientSession created
    │
    ▼
ConnectionManager.connect()
    │
    ▼
Broadcast join event
```
---
```
Failed Connection

Client
    │
    ▼
WebSocket Handshake
    │
    ▼
Server accepts connection
    │
    ▼
Validation fails
    │
    ▼
ERROR message sent
    │
    ▼
WebSocket closed
    │
    ▼
Connection terminated
```
---

# ClientSession

Every connected client is represented by a ClientSession.

Fields

- username
- websocket

---

# Message Format

(Current Version)

Messages are plain UTF-8 text.

#### Example
```
Hello Everyone
```
---

# Broadcast Types

## Broadcast

Sent to every connected client.

#### Example
```
Bharat: Hello Everyone
```
---

## Broadcast Except

Sent to every connected client except one.

Used for

- Join notifications
- Leave notifications

#### Example
```
📢 Bharat joined the chat.
```
#### Example
```
📢 Bharat left the chat.
```
---

# Current Server Events

Join
```
📢 <username> joined the chat.
```
Sent to

All connected clients except the joining client.

---

Leave
```
📢 <username> left the chat.
```
Sent to

All connected clients except the leaving client.

---

Chat
```
<username>: <message>
```
Sent to

All connected clients except the sender.

---

# Design Principles

NexusChat evolves incrementally.

Rules

- Build only for today's requirements.
- Introduce abstractions only when required.
- Prefer simple implementations over speculative designs.
- Refactor only when patterns naturally emerge.

---

# Future Extensions

Planned

- Structured JSON protocol
- Private messaging
- Chat rooms
- Presence
- Typing indicators
- Authentication
- JWT
- Redis Pub/Sub
- Horizontal scaling