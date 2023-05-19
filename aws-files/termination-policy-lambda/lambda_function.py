import boto3
import datetime

def lambda_handler(event, context):
    instances = event.get('Instances')

    min_metric_value = float('inf')
    min_metric_instance_id = None

    now = datetime.datetime.utcnow()

    for instance in instances:
        instance_id = instance['InstanceId']

        response = boto3.client('cloudwatch').get_metric_statistics(
            Namespace='Snake',
            MetricName='PlayerCount',
            Dimensions=[
                {
                    'Name':  'InstanceId',
                    'Value': instance_id
                },
                {
                    'Name':  'AutoScalingGroupName',
                    'Value': 'snake-asg'
                }
            ],
            StartTime=now-datetime.timedelta(seconds=30),
            EndTime=now,
            Period=1,
            Statistics=['Average']
        )

        datapoints = response['Datapoints']
        datapoints_sorted = sorted(datapoints, key=lambda x: x['Timestamp'], reverse=True)
        
        metric_value = datapoints_sorted[0]['Average']

        if metric_value < min_metric_value:
            min_metric_value = metric_value
            min_metric_instance_id = instance_id

    print("Minimum metric instance id: ", min_metric_instance_id)

    json_data = {
        "InstanceIDs": [min_metric_instance_id]
    }

    return json_data
