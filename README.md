# Script 1: AWS Boto3: Single-Region EC2 Inventory Script

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


## Script 3: Single-Region EC2 and RDS Inventory (`region_ec2_rds_inventory.py`)

### Overview
A Python automation script utilizing the Boto3 SDK to programmatically audit both EC2 virtual machines and RDS relational databases within the session's active default region. It extracts key operational details such as instance IDs, hardware configurations, power states, database engines, statuses, and custom Name tags in a single unified report.

### Usage
Run the script from an authenticated terminal session:
(bash)
python3 region_ec2_rds_inventory.py



## Script 4: Global Multi-Region EC2 and RDS Inventory (`global_ec2_rds_inventory.py`)

### Overview
An advanced automation script that dynamically discovers all active AWS regions globally using the `describe_regions` API. It systematically loops through every region in the account to audit and aggregate both EC2 virtual machines and RDS relational databases worldwide, outputting a structured region-by-region report complete with instance states, database engines, and custom tags.

### Usage
Run the global infrastructure audit script from an authenticated terminal session:
(bash)
python3 global_ec2_rds_inventory.py



## Script 5: Single-Region ECS Cluster and Task Inventory (`ecs_inventory.py`)

### Overview
A Python automation script utilizing the Boto3 SDK to programmatically audit Amazon ECS clusters, registered container instances, and active running tasks within the session's active default region. It extracts cluster health statuses, underlying EC2 instance mappings, launch types, and task execution states into a structured report.

### Usage
Run the script from an authenticated terminal session:
(bash)
python3 ecs_inventory.py
