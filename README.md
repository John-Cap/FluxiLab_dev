# FluxiLab_dev

## Overview

This project implements a secure, centralized access system for interacting with laboratory equipment hosted on isolated Raspberry Pi devices. Users and administrators connect through a web-based interface served over the organizational network. From this portal, authenticated users are routed to specific Flutter-based user interfaces hosted on the Raspberry Pis.

Communication between the frontend and backend is handled entirely through MQTT, promoting a decoupled and asynchronous architecture. Each Raspberry Pi exists behind an isolated router on its own subnet, with access provided through configured WAN port forwarding.

## Project Goals

- Provide a secure login system for users and administrators.
- List and route users to specific fumehoods (router + Raspberry Pi) based on their role.
- Implement an administrator interface to modify system settings and metadata.
- Use MQTT as the sole transport layer for client-backend communication.
- Maintain separation of concerns across application layers.

## Current Status

Project planning and architecture design are in progress. Development has not yet begun.

Refer to the detailed architecture document at `docs/DESIGN.md`.

## Technology Stack

| Layer             | Technology             |
|------------------|------------------------|
| Frontend UI       | Flutter Web            |
| Backend Services  | Python (asynchronous)  |
| Communication     | MQTT (Mosquitto 2.x)  |
| Database          | MySQL    |
| Edge Devices      | Raspberry Pi |
| Routing Layer     | Static port forwarding via router configuration |
| Deployment Tools  | Python served, cloud based |

## Directory Structure

├── backend/ # Python backend services
├── flutter_web/ # Flutter web portal
├── docs/ # Design documentation
│ └── DESIGN.md
├── database/ # Schema definitions and migration files
├── infrastructure/ # Deployment scripts, network config
└── README.md


## Contributor

Author: Wessel Bonnet
Role: System Architect and Full-Stack Developer

## License

This repository is currently private and intended for development and educational use. A formal license will be added at a later stage.
