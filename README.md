# AWS Boto3: Single-Region EC2 Inventory Script

## Overview
A Python script utilizing the Boto3 SDK to programmatically scan a specified AWS region (in this case, the account's default region), list all provisioned EC2 instances, and extract key operational metrics including instance ID, hardware type, power state, and custom Name tags.

## Usage
Run the script from an authenticated terminal session:
```bash
python3 ec2_inventory.py
