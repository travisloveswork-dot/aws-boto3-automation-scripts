import boto3

# Define your target AWS region
REGION = 'us-east-1'

print(f"=== AWS Infrastructure Audit (EC2 & RDS) in Region: {REGION} ===\n")

# 1. Audit EC2 Instances
print("--- EC2 Instances ---")
ec2 = boto3.resource('ec2', region_name=REGION)
ec2_count = 0

for instance in ec2.instances.all():
    ec2_count += 1
    print(f"  -> Instance ID: {instance.id}")
    print(f"     Type: {instance.instance_type}")
    print(f"     State: {instance.state['Name']}")
    
    # Extract custom Name tag if assigned
    name = "No Name Tag Assigned"
    if instance.tags:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
    print(f"     Name: {name}")
    print("-" * 30)

print(f"Total EC2 instances found: {ec2_count}\n")

# 2. Audit RDS Instances
print("--- RDS Database Instances ---")
rds_client = boto3.client('rds', region_name=REGION)
rds_count = 0

try:
    response = rds_client.describe_db_instances()
    db_instances = response.get('DBInstances', [])
    
    for db in db_instances:
        rds_count += 1
        print(f"  -> DB Identifier: {db['DBInstanceIdentifier']}")
        print(f"     Engine: {db['Engine']} (Version: {db['EngineVersion']})")
        print(f"     Status: {db['DBInstanceStatus']}")
        print(f"     Instance Class: {db['DBInstanceClass']}")
        print("-" * 30)
        
except Exception as e:
    print(f"Error fetching RDS instances: {e}")

print(f"Total RDS instances found: {rds_count}")
print("\nAudit Complete.")
