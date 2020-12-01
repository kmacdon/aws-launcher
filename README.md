# AWS Launcher

This project is a command line tool to launch AWS EC2 instances easily. It uses the boto3 package to launch the instance with an AMI I created that has Docker installed and a docker container I created based off of the jupyter/datascience-notebook docker image. This container launches jupyter lab and is password protected based on the jupyter config file I passed to the docker image I made when building it.

### Instructions

```
start_aws--size <size>
```

The size argument determines how big of an ec2 instance to launch, acceptable sizes being small, medium, or large. If no size is given, it launches a t2.micro instance as a test run.

The script will print out the ssh command to login into the server; in the home folder of the server, there is a file called `start_jupyter.sh` which launches the docker container for jupyter.
