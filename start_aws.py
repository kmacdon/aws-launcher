import argparse
from launcher import Launcher

parser = argparse.ArgumentParser(description='Launch an ec2 instance')
parser.add_argument('--size', '-s', type=str, nargs='?', default='test')

args = parser.parse_args()

launcher = Launcher()
image_id = launcher.launch_instance(args.size)

stop = "no"
while stop != "yes":
    stop = input("Stop Instance?")

launcher.stop_instance(image_id)
