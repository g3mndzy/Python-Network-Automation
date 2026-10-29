
# Python Network Automation Lab

## Overview

Built Python scripts to automate routine network administration tasks, including device inventory, connectivity testing, DNS monitoring, email alerts, support ticket management, and configuration backups.

## Project Sections

### 1. Device Inventory
Reads device information from a CSV file and lists the devices used for monitoring.

**Files:** `network_devices.csv`, `list_devices.py`, `T2_read_network_devices.py`

### 2. Connectivity Monitoring
Checks device availability using ping to identify devices that may require attention.

**Files:** `ping_devices.py`, `StepC2_device_ping.py`

### 3. Email Notifications
Sends notifications about device availability and DNS issues, with follow-up messages for resolved problems.

**Files:** `T2_device_availability_email.py`, `T2_DNS_Email_Alert_Test.py`, `resolution_email_part_2.py`

### 4. DNS Monitoring and Correction
Checks internal DNS settings, identifies unexpected configurations, and uses Netmiko to connect to devices and correct settings.

**Files:** `check_internal_dns.py`, `connect_correct_dns.py`, `T2_DNS_Setting_Altered.py`

### 5. Support Ticket Management
Uses API requests to create and update support tickets associated with detected network issues.

**Files:** `create_ticket.py`, `StepC4_Ticket_Creation.py`, `T2_ticket_creation.py`, `T2_update_ticket`

### 6. Backup Preparation and Logging
Creates a directory for backups and records DNS monitoring results for troubleshooting.

**Files:** `create_backup_directory.py`, `StepC5_dns_log.py`, `dns_status.log`

## Tools and Technologies

Python • Netmiko • REST APIs • SMTP • CSV • DNS • Linux

## Skills Developed

- Automating repetitive network administration tasks
- Monitoring device connectivity and DNS configurations
- Connecting to devices for configuration remediation
- Integrating email notifications and support ticket workflows
- Recording results to support troubleshooting
