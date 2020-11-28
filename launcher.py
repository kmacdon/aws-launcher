import boto3
import json
import time
from ssh_client import SSH

class Launcher:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.ssh = None

    def launch_instance(self, size, version):
        with open("base_config.json") as f:
            config = json.load(f)

        if size == "small":
            config['InstanceType'] = "m4.xlarge"
        elif size == "medium":
            config['InstanceType'] = "m4.2xlarge"
        elif size == "large":
            config['InstanceType'] = "m4.4xlarge"

        yaml_file = 'jupyter-comp.yaml' if version == 'python' else 'rstudio-comp.yaml'
        print("Launching instance...")
        result = self.ec2.run_instances(**config)
        image_id = result['Instances'][0]['InstanceId']

        count = 0
        status = 'launching'

        while status != 'running':
            count += 1
            if count > 100:
                Exception('Could not connect to instance.')

            info = self.ec2.describe_instances(InstanceIds=[image_id])
            status = info['Reservations'][0]['Instances'][0]['State']['Name']
            time.sleep(5)

        public_dns = info['Reservations'][0]['Instances'][0]['PublicDnsName']

        print("Uploading files...")
        self.ssh = SSH("/Users/kevinmacdonald/.ssh/aws_key.pem", "ubuntu", public_dns)
        self.ssh.upload_files([yaml_file])
        self.ssh.upload_files(["aws_credentials.env"])
        self.ssh.upload_files(["aws_credentials"])
        self.ssh.upload_files(["rstudio-password"])
        self.ssh.upload_files(["/Users/kevinmacdonald/.ssh/aws_git"])

        print("Launching docker...")
        self.ssh.execute_commands([
            "sudo docker swarm init",
            f"sudo docker stack deploy -c {yaml_file} jup"
            ])

        print(f"ssh -i ~/.ssh/aws_key.pem ubuntu@{public_dns}")
        print(public_dns)

        return image_id, public_dns

    def stop_instance(self, image_id):
        self.ssh.execute_commands([
            "sudo docker stack rm jup"
            ])
        self.ec2.terminate_instances(InstanceIds=[image_id])

