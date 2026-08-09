import boto3

# Step 1: Get a list of all active AWS regions dynamically
client = boto3.client('ec2', region_name='us-east-1')
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

print("=== Global Multi-Region ECS Inventory Audit ===")
print(f"Scanning {len(regions)} regions worldwide for ECS resources...\n")

total_global_clusters = 0
total_global_container_instances = 0
total_global_tasks = 0

for region in regions:
    print(f"==================================================")
    print(f"Region: {region}")
    print(f"==================================================")

    try:
        ecs_client = boto3.client('ecs', region_name=region)
        clusters_response = ecs_client.list_clusters()
        cluster_arns = clusters_response.get('clusterArns', [])
        
        if cluster_arns:
            print(f"  [ECS] {len(cluster_arns)} cluster(s) found:")
            total_global_clusters += len(cluster_arns)
            
            for cluster_arn in cluster_arns:
                cluster_desc = ecs_client.describe_clusters(clusters=[cluster_arn])
                cluster_info = cluster_desc['clusters'][0]
                cluster_name = cluster_info['clusterName']
                
                print(f"    -> Cluster: {cluster_name}")
                print(f"       Status: {cluster_info['status']}")
                
                # Container Instances
                ci_response = ecs_client.list_container_instances(cluster=cluster_arn)
                ci_arns = ci_response.get('containerInstanceArns', [])
                if ci_arns:
                    total_global_container_instances += len(ci_arns)
                    ci_details = ecs_client.describe_container_instances(
                        cluster=cluster_arn,
                        containerInstances=ci_arns
                    )
                    print(f"       [Container Instances] ({len(ci_arns)} found):")
                    for ci in ci_details.get('containerInstances', []):
                        print(f"         - Container Instance ID: {ci['containerInstanceArn'].split('/')[-1]}")
                        print(f"           EC2 Instance ID: {ci.get('ec2InstanceId', 'N/A')}")
                        print(f"           Status: {ci['status']}")
                
                # Running Tasks
                tasks_response = ecs_client.list_tasks(cluster=cluster_arn, desiredStatus='RUNNING')
                task_arns = tasks_response.get('taskArns', [])
                if task_arns:
                    total_global_tasks += len(task_arns)
                    task_details = ecs_client.describe_tasks(
                        cluster=cluster_arn,
                        tasks=task_arns
                    )
                    print(f"       [Running Tasks] ({len(task_arns)} found):")
                    for task in task_details.get('tasks', []):
                        print(f"         - Task ID: {task['taskArn'].split('/')[-1]}")
                        print(f"           Launch Type: {task.get('launchType', 'N/A')}")
                        print(f"           Last Status: {task['lastStatus']}")
        else:
            print("  [ECS] No clusters found.")
            
    except Exception as e:
        print(f"  [ECS] Error scanning region {region}: {e}")
    
    print()

print("==================================================")
print(f"Global Audit Complete.")
print(f"Total Clusters found worldwide: {total_global_clusters}")
print(f"Total Container Instances found worldwide: {total_global_container_instances}")
print(f"Total Running Tasks found worldwide: {total_global_tasks}")
