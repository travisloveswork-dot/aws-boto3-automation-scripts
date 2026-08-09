import boto3

# Step 1: Get a list of all active AWS regions dynamically
client = boto3.client('ec2', region_name='us-east-1')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print("=== Global AWS EC2 Inventory Audit (All Regions) ===")
print(f"Scanning {len(regions)} regions for resources...\n")

total_global_instances = 0

for region in regions:
    try:
        # Dynamically re-initialize the EC2 resource for each region
        ec2 = boto3.resource('ec2', region_name=region)
        instances = list(ec2.instances.all())
        
        if instances:
            print(f"Region: {region} ({len(instances)} instance(s) found)")
            for instance in instances:
                total_global_instances += 1
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
                print("-" * 35)
                
    except Exception as e:
        # Skip regions with opt-in restrictions or access limits
        print(f"Skipping region {region} due to an error: {e}")

print(f"\nGlobal Audit Complete. Total instances found across all regions: {total_global_instances}")
