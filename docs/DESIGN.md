# Software Design Document

## Project: Laboratory Access Routing System

**Author:** Wessel Bonnet  
**Version:** 1.0  
**Last Updated:** 2025/06/19

---

## 1. Project Overview

This project provides a centralized, secure web interface for accessing laboratory equipment hosted on Raspberry Pi devices, each isolated behind its own router. The system enables users and administrators to interact with these devices via a Flutter web application that communicates with a Python backend over MQTT.

The system routes users through a secure organizational network to the correct Raspberry Pi by resolving mapped router ports, while enforcing role-based access and maintaining clean separation between concerns.

---

## 2. Functional Objectives

### 2.1 User Capabilities
- Authenticate via a central Flutter web UI.
- View and select a specific fumehood (router + Raspberry Pi).
- Be redirected to the selected Pi's Flutter UI (hosted locally on the Pi).

### 2.2 Administrator Capabilities
- Perform all user actions.
- Access a secure admin dashboard.
- View and modify database records (CRUD).
- Manage routing and system configuration.

---

## 3. Architectural Design

### 3.1 High-Level Component Overview

User (Org Network)
↓
Flutter Web (Frontend)
↓
MQTT Broker
↓
Python Backend
↓
Database & Routing Map
↓
Router WAN Port Forwarding
↓
Raspberry Pi Web Server


### 3.2 Technologies

| Layer             | Technology        |
|------------------|-------------------|
| Frontend UI       | Flutter (Web)     |
| Backend Logic     | Python (async)    |
| Messaging Layer   | MQTT (EMQX/Mosquitto) |
| Database          | PostgreSQL/MySQL  |
| Edge Devices      | Raspberry Pi + Flutter |
| Network Routing   | Static IP + Port Forwarding |
| Deployment        | Docker (optional), NGINX (optional) |

---

## 4. Communication Model

### 4.1 MQTT Topic Structure

| Direction          | Topic                         | Payload Format                 |
|--------------------|-------------------------------|--------------------------------|
| UI → Backend       | `frontend/login/request`      | `{username, password}`         |
| Backend → UI       | `backend/login/response`      | `{status, role, token}`        |
| UI → Backend       | `frontend/fumehoods/request`  | `{token}`                      |
| Backend → UI       | `backend/fumehoods/response`  | `{id, label, redirect_url}`    |

- All communication between the UI and backend occurs via the MQTT broker.
- Topics are namespaced and restricted based on roles and tokens.

---

## 5. Module Responsibilities

### 5.1 Frontend (Flutter Web)
- Provides login interface and routing dashboard.
- Displays available fumehoods dynamically.
- Performs redirection to selected Pi’s web UI.
- Subscribes/publishes to MQTT using `mqtt_client`.

### 5.2 Backend (Python)
- Subscribes to MQTT topics to handle authentication, routing, and admin actions.
- Interfaces with the database using an ORM.
- Publishes validated responses to appropriate MQTT response topics.
- Enforces role-based access control.

### 5.3 Database
- Stores user credentials and role metadata.
- Stores router → Pi mappings with WAN port associations.
- Records lab device configurations and experiment metadata.

### 5.4 Raspberry Pi Devices
- Serve localized Flutter UIs for device interaction.
- Remain isolated per-router with fixed internal IPs (192.168.1.x).
- Exposed via dedicated port forwarding on router WAN interface.

---

## 6. Security Model

- All MQTT messages use TLS for encryption.
- Role-based access (admin/user) enforced at backend level.
- Token-based session validation (JWT or similar).
- Minimal network exposure: Only necessary ports are forwarded.
- No direct database access from frontend.

---

## 7. Implementation Phases

| Phase | Description                              |
|-------|------------------------------------------|
| 1     | Implement backend authentication logic   |
| 2     | Integrate Flutter frontend with MQTT     |
| 3     | Develop fumehood routing mechanism       |
| 4     | Build admin dashboard and CRUD tools     |
| 5     | Secure MQTT and configure TLS            |
| 6     | Deploy to server and configure Pis       |
| 7     | Write tests and deploy monitoring        |

---

## 8. Testing & Validation

- **Unit Tests:** Python service modules (auth, db logic)
- **Integration Tests:** MQTT message-response chains
- **Frontend Tests:** Flutter widget and logic tests
- **End-to-End Tests:** Full login → Pi redirect experience
- **Security Testing:** TLS verification, role enforcement

---

## 9. Success Criteria

A successful implementation will meet the following conditions:

| Domain           | Success Indicator                                             |
|------------------|---------------------------------------------------------------|
| Functionality     | Users and admins can log in and reach Pi interfaces securely |
| Reliability       | MQTT handles concurrent requests without loss                |
| Security          | All communications are authenticated and encrypted           |
| Scalability       | New Pis or fumehoods added without codebase refactor         |
| Maintainability   | Code is modular, documented, and test-covered                |
| Deployability     | System runs on Docker or bare metal with minimal setup       |

---

## 10. Future Enhancements

- Central logging and metrics (e.g., Prometheus, Grafana).
- Dynamic device registration (Pi self-registers via MQTT).
- Real-time control features from web to equipment.
- WebSocket fallback or REST layer for redundancy.

---
