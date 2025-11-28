# 📡 Surrounded

A lightweight and fast local network scanner written in **Python**.
**Surrounded** uses the **ARP** (Address Resolution Protocol) to discover all devices connected to your network, displaying their **IP** and **MAC** addresses in a clean table format.

Perfect for system administrators, cybersecurity students, or anyone wanting to see who is connected to their Wi-Fi.

## 🚀 Features

- **ARP Scanning:** Uses ARP broadcast packets for accurate detection on local networks (LAN).
- **CLI Interface:** Simple and fast usage from the terminal.
- **Clean Output:** Displays results in an organized table.
- **Lightweight:** Depends only on the `scapy` library.

## 📋 Prerequisites

- **Python 3.x**
- **Administrator/Root privileges** (required to send network packets).

## 🛠️ Installation

1. **Clone this repository:**

2.  **Install dependencies:**

    *For Linux (Debian/Ubuntu/Kali - Recommended):*

    ```
    sudo apt update
    sudo apt install python3-scapy
    ```

    *For Windows or Virtual Environments:*

    ```
    pip install scapy
    ```

## 💻 Usage

The tool needs to be run with superuser privileges because it manipulates the network card.

### Basic Syntax

```bash
sudo python3 surrounded.py -t <IP_RANGE>
```

### Arguments

  - `-t` or `--target`: Specify the target IP or IP range (CIDR format).

### Examples

**Scan the entire local network (Common Class C):**

```bash
sudo python3 surrounded.py -t 192.168.1.1/24
```

**Scan a specific network:**

```
sudo python3 surrounded.py -t 10.0.0.1/24
```

## 🖼️ Output Example

```text
[*] Scanning network: 192.168.1.1/24 ...

--------------------------------------------------
IP Address              MAC Address
--------------------------------------------------
192.168.1.1             a4:91:b1:xx:xx:xx
192.168.1.15            bc:d1:12:xx:xx:xx
192.168.1.22            00:e0:4c:xx:xx:xx
--------------------------------------------------
```

## ⚠️ Legal Disclaimer

**For educational purposes only.**
This tool is intended to be used on networks you own or have explicit permission to test. The author is not responsible for any misuse of this software.

## 🗺️ Roadmap

  -  Vendor detection (Samsung, Apple, etc.) based on MAC address.
  -  Export results to file (CSV/TXT).
  -  Web Interface using Flask.

## ❓How does it works? 

This tool discovers devices by using the **Address Resolution Protocol (ARP)**, which operates at **Layer 2 (Data Link Layer)** of the OSI model. It broadcasts requests to resolve IP addresses to MAC addresses.

![osi-model-1569501229-1](https://github.com/user-attachments/assets/e30844ec-29a1-4c9e-9307-7a036d390143)


Unlike **Layer 3 (Network Layer)** protocols such as ICMP (Ping), which are often blocked by host-based firewalls (like Windows Defender), ARP traffic cannot be blocked without breaking basic local network connectivity. Since Layer 2 resolution is a prerequisite for Layer 3 communication, devices are forced to process these packets, making this scanning method highly reliable.
