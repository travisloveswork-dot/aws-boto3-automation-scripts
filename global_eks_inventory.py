import boto3

# Step 1: Get a list of all active AWS regions dynamically
client = boto3.client('ec2', region_name='us-east-1')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print("=== Global Multi-Region EKS Cluster Inventory Audit ===")
print(f"Scanning {len(regions)} regions worldwide for EKS clusters...\n")

total_global_clusters = 0

for region in regions:
    print(f"==================================================")
    print(f"Region: {region}")
    print(f"==================================================")

    try:
        eks_client = boto3.client('eks', region_name=region)
        response = eks_client.list_clusters()
        cluster_names = response.get('clusters', [])
        
        if cluster_names:
            print(f"  [EKS] {len(cluster_names)} cluster(s) found:")
            total_global_clusters += len(cluster_names)
            
            for cluster_name in cluster_names:
                try:
                    cluster_desc = eks_client.describe_cluster(name=cluster_name)
                    cluster = cluster_desc['cluster']
                    
                    print(f"    -> Cluster Name: {cluster['name']}")
                    print(f"       Status: {cluster['status']}")
                    print(f"       Kubernetes Version: {cluster.get('version', 'N/A')}")
                    print(f"       Endpoint: {cluster.get('endpoint', 'N/A')}")
                    print(f"       Role ARN: {cluster.get('roleArn', 'N/A')}")
                    print(f"       Creation Time: {cluster.get('createdAt', 'N/A')}")
                except Exception as e:
                    print(f"       Error describing cluster {cluster_name}: {e}")
        else:
            print("  [EKS] No clusters found.")
            
    except Exception as e:
        print(f"  [EKS] Error scanning region {region}: {e}")
    
    print()

print("==================================================")
print(f"Global Audit Complete.")
print(f"Total EKS clusters found worldwide: {total_global_clusters}")
