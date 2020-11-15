import boto3
import json
import time

class Launcher:
    def init(self):
        self.ec2 = boto3.client('ec2')

    def launch_instance(self):
        with open("base_config.json") as f:
            config = json.load(f)

        result = self.ec2.run_instances(**config)
        image_id = result['Instances'][0]['InstanceId']

        status = 'launching'
        count = 0

        while status != 'running':
            count += 1
            if count > 100:
                Exception('Could not connect to instance.')

            info = self.ec2.describe_instances(InstanceIds=image_id)
            status = info['Reservations'][0]['Instances'][0]['State']['Name']
            time.sleep(5)

        public_dns = info['Reservations'][0]['Instances'][0]['PublicDnsName']

    def stop_instance(id):
        self.ec2.terminate_instances(InstanceIds=image_id)

