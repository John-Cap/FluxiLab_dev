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

