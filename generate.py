import os
import json
import sys

cluster = sys.argv[1]
repository = sys.argv[2]
services = os.popen('aws ecs list-services --cluster {}'.format(cluster)).read()
service = [service.split('/')[-1] for service in json.loads(services)['serviceArns'] if repository.replace('code-commit-wise-bsw-', '') in service][0]
service_describe = os.popen('aws ecs describe-services --region  ap-northeast-1 --cluster {}  --services {}'.format(cluster, service)).read()
taskDefinition = json.loads(service_describe)['services'][0]['taskDefinition'].split('/')[-1]
task_describe = os.popen('aws ecs describe-task-definition --region ap-northeast-1  --task-definition {}'.format(taskDefinition)).read()
task_data = json.loads(task_describe)

task_define = {
    "family": "",
    "taskRoleArn": "",
    "executionRoleArn": "",
    "networkMode": "",
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "",
    "memory": "",
    "volumes": "",
    "containerDefinitions": ""
}

task_define['family'] = task_data['taskDefinition']['family']
task_define['taskRoleArn'] = task_data['taskDefinition']['taskRoleArn']
task_define['executionRoleArn'] = task_data['taskDefinition']['executionRoleArn']
task_define['networkMode'] = task_data['taskDefinition']['networkMode']
task_define['cpu'] = task_data['taskDefinition']['cpu']
task_define['memory'] = task_data['taskDefinition']['memory']
task_define['volumes'] = task_data['taskDefinition']['volumes']
# name = json.loads(service_describe)['services'][0]['serviceName']
task_define['containerDefinitions'] = task_data['taskDefinition']['containerDefinitions']
for container in task_data['taskDefinition']['containerDefinitions']:
    if str(container['name']).endswith('spr') or str(container['name']).endswith('ngx'):
        container['image'] = "<IMAGE1_NAME>"
        name = container['name']
        print(name)
json_str = json.dumps(task_define, indent=4)

# generate TaskDifinition.json
with open('TaskDifinition.json', 'w') as f:
    f.write(json_str)

# generate appspec.yaml
data = {
    "version": "0.0",
    "Resources": [
        {"TargetService": {
            "Type": "AWS::ECS::Service",
            "Properties": {
                "TaskDefinition": "<TASK_DEFINITION>",
                "LoadBalancerInfo": {
                    "ContainerName": name,
                    "ContainerPort": 80
                },
                "PlatformVersion": "1.4.0"
            }
        }
         }
    ]
}

with open('appspec.json', 'w') as f:
    print(json.dumps(data, indent=4), file=f)
