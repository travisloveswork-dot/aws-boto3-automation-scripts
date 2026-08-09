import boto3

print("=== AWS ECS Inventory Audit (Default Region) ===\n")

# Boto3 automatically targets the account's default region from your environment/config
ecs_client = boto3.client('ecs')
cluster_count = 0
instance_count = 0
task_count = 0

try:
    # 1. List all ECS Clusters
    clusters_response = ecs_client.list_clusters()
    cluster_arns = clusters_response.get('clusterArns', [])
    
    if not cluster_arns:
        print("No ECS clusters found in the default region.")
    else:
        cluster_count = len(cluster_arns)
        print(f"Found {cluster_count} ECS Cluster(s). Scanning details...\n")
        
        for cluster_arn in cluster_arns:
            # Get cluster details
            cluster_desc = ecs_client.describe_clusters(clusters=[cluster_arn])
            cluster_info = cluster_desc['clusters'][0]
            cluster_name = cluster_info['clusterName']
            
            print(f"==================================================")
            print(f"Cluster: {cluster_name}")
            print(f"Status: {cluster_info['status']}")
            print(f"==================================================")
            
            # 2. List Container Instances (for EC2 launch type)
            ci_response = ecs_client.list_container_instances(cluster=cluster_arn)
            ci_arns = ci_response.get('containerInstanceArns', [])
            
            if ci_arns:
                ci_details = ecs_client.describe_container_instances(
                    cluster=cluster_arn,
                    containerInstances=ci_arns
                )
                print(f"  [Container Instances] {len(ci_arns)} found:")
                for ci in ci_details.get('containerInstances', []):
                    instance_count += 1
                    print(f"    -> Container Instance ID: {ci['containerInstanceArn'].split('/')[-1]}")
                    print(f"       EC2 Instance ID: {ci.get('ec2InstanceId', 'N/A')}")
                    print(f"       Status: {ci['status']}")
                    print(f"       Running Tasks: {ci['runningTasksCount']}")
            else:
                print("  [Container Instances] None registered (or using Fargate).")
            
            # 3. List Running Tasks
            tasks_response = ecs_client.list_tasks(cluster=cluster_arn, desiredStatus='RUNNING')
            task_arns = tasks_response.get('taskArns', [])
            
            if task_arns:
                task_details = ecs_client.describe_tasks(
                    cluster=cluster_arn,
                    tasks=task_arns
                )
                print(f"  [Running Tasks] {len(task_arns)} found:")
                for task in task_details.get('tasks', []):
                    task_count += 1
                    print(f"    -> Task ID: {task['taskArn'].split('/')[-1]}")
                    print(f"       Launch Type: {task.get('launchType', 'N/A')}")
                    print(f"       Last Status: {task['lastStatus']}")
                    print(f"       Desired Status: {task['desiredStatus']}")
            else:
                print("  [Running Tasks] No running tasks found.")
            
            print()

except Exception as e:
    print(f"Error fetching ECS resources: {e}")

print("==================================================")
print(f"Audit Complete.")
print(f"Total Clusters: {cluster_count}")
print(f"Total Container Instances: {instance_count}")
print(f"Total Running Tasks: {task_count}")
