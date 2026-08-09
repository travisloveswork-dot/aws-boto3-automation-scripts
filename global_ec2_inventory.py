import boto3

# Step 1: Get a list of all active AWS regions dynamically
client = boto3.client('ec2', region_name='us-east-1')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print("=== Global Multi-Region EC2 Inventory Audit ===")
print(f"Scanning {len(regions)} regions worldwide for EC2 instances...\n")

total_global_ec2 = 0

for region in regions:
    print(f"==================================================")
    print(f"Region: {region}")
    print(f"==================================================")

    try:
        ec2 = boto3.resource('ec2', region_name=region)
        instances = list(ec2.instances.all())
        
        if instances:
            print(f"  [EC2] {len(instances)} instance(s) found:")
            for instance in instances:
                total_global_ec2 += 1
                print(f"    -> Instance ID: {instance.id}")
                print(f"       Type: {instance.instance_type}")
                print(f"       State: {instance.state['Name']}")
                
                # Extract custom Name tag if assigned
                name = "No Name Tag Assigned"
                if instance.tags:
                    for tag in instance.tags:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                print(f"       Name: {name}")
        else:
            print("  [EC2] No instances found.")
    except Exception as e:
        print(f"  [EC2] Error scanning region {region}: {e}")
    
    print()

print("==================================================")
print(f"Global Audit Complete.")
print(f"Total EC2 instances found worldwide: {total_global_ec2}")
