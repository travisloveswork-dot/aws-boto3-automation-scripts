import boto3

# Initialize the EC2 resource in your default region
ec2 = boto3.resource('ec2')

print("=== AWS EC2 Inventory Audit ===")
print("Scanning your account for EC2 instances...\n")

instance_count = 0

# Iterate through every EC2 instance in the account
for instance in ec2.instances.all():
    instance_count += 1
    print(f"Instance ID: {instance.id}")
    print(f"Instance Type: {instance.instance_type}")
    print(f"Current State: {instance.state['Name']}")
    
    # Extract the 'Name' tag if it exists
    name = "No Name Tag Assigned"
    if instance.tags:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
    print(f"Instance Name: {name}")
    print("-" * 40)

print(f"Audit Complete. Total instances found: {instance_count}")
