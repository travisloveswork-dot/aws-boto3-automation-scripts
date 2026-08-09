import boto3

print("=== AWS EKS Cluster Inventory Audit (Default Region) ===\n")

# Boto3 automatically targets the account's default region from your environment/config
eks_client = boto3.client('eks')
cluster_count = 0

try:
    # 1. List all EKS Clusters
    response = eks_client.list_clusters()
    cluster_names = response.get('clusters', [])
    
    if not cluster_names:
        print("No EKS clusters found in the default region.")
    else:
        cluster_count = len(cluster_names)
        print(f"Found {cluster_count} EKS Cluster(s). Scanning details...\n")
        
        for cluster_name in cluster_names:
            try:
                # 2. Get detailed information for each cluster
                cluster_desc = eks_client.describe_cluster(name=cluster_name)
                cluster = cluster_desc['cluster']
                
                print(f"==================================================")
                print(f"Cluster Name: {cluster['name']}")
                print(f"Status: {cluster['status']}")
                print(f"Kubernetes Version: {cluster.get('version', 'N/A')}")
                print(f"Endpoint: {cluster.get('endpoint', 'N/A')}")
                print(f"Role ARN: {cluster.get('roleArn', 'N/A')}")
                print(f"Creation Time: {cluster.get('createdAt', 'N/A')}")
                print(f"==================================================")
                print()
            except Exception as e:
                print(f"Error describing cluster {cluster_name}: {e}")
                
except Exception as e:
    print(f"Error fetching EKS clusters: {e}")

print(f"Audit Complete. Total EKS clusters found: {cluster_count}")
