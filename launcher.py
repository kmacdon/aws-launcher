import boto3
import json
import time

class Launcher:
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def launch_instance(self, size):
        with open("base_config.json") as f:
            config = json.load(f)

        result = self.ec2.run_instances(**config)
        image_id = result['Instances'][0]['InstanceId']

        if size == "small":
            config['InstanceType'] = "m4.large"
        elif size == "medium":
            config['InstanceType'] = "m4.xlarge"
        elif size == "large":
            config['InstanceType'] = "m4.4xlarge"

        status = 'launching'
        count = 0

        while status != 'running':
            count += 1
            if count > 100:
                Exception('Could not connect to instance.')

            info = self.ec2.describe_instances(InstanceIds=[image_id])
            status = info['Reservations'][0]['Instances'][0]['State']['Name']
            time.sleep(5)

        public_dns = info['Reservations'][0]['Instances'][0]['PublicDnsName']

        print(f"ssh -i ~/.ssh/aws_key.pem ubuntu@{public_dns}")
        print(public_dns)

        return image_id

    def stop_instance(self, image_id):
        self.ec2.terminate_instances(InstanceIds=[image_id])

