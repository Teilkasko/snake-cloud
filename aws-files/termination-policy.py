import boto3
import json
import datetime

def lambda_handler(event, context):
    # Extract relevant information from the input event
    data = json.loads(event)

    instances = event['Instances']

    # Initialize variables to keep track of the minimum metric value and its corresponding instance ID
    min_metric_value = float('inf')
    min_metric_instance_id = None

    now = datetime.datetime.utcnow()

    # Iterate over each instance in the input event
    for instance in instances:
        instance_id = instance['InstanceId']

        # Query the CloudWatch metric for the current instance ID
        response = boto3.client('cloudwatch').get_metric_statistics(
            Namespace='Snake',
            MetricName='PlayerPercentage',
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
            Period=1
        )

        # Check if the metric data exists and retrieve the average metric value
        datapoints = response['Datapoints']
        if datapoints:
            metric_value = datapoints[0]['PlayerPercentage']

            # Update the minimum metric value and corresponding instance ID if necessary
            if metric_value < min_metric_value:
                min_metric_value = metric_value
                min_metric_instance_id = instance_id


    # Create the JSON structure
    json_data = {
        "InstanceIDs": [min_metric_instance_id]
    }


    # Return the instance ID with the lowest metric value
    return json.dumps(json_data, indent=4)
