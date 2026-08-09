# AWS Boto3: Single-Region EC2 Inventory Script

## Overview
A Python script utilizing the Boto3 SDK to programmatically scan a specified AWS region (in this case, the account's default region), list all provisioned EC2 instances, and extract key operational metrics including instance ID, hardware type, power state, and custom Name tags.

## Usage
Run the script from an authenticated terminal session:
(bash)
python3 ec2_inventory.py

## Script 2: Global Multi-Region EC2 Inventory

### Overview
An advanced automation script using Boto3's `describe_regions` API to dynamically discover every active AWS region. It loops through each region to aggregate and display running EC2 virtual machines worldwide within the target account, complete with instance states, hardware types, and custom Name tags.

### Usage
Run the global audit script from your terminal:
(bash)
python3 global_ec2_inventory.py
