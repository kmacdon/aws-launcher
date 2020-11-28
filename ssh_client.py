# https://hackersandslackers.com/automate-ssh-scp-python-paramiko/
from paramiko import SSHClient, RSAKey, AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError
from scp import SCPClient
from os import system

class SSH:
    def __init__(self, key, user, host):
        self.filepath = key
        self.user = user
        self.host = host
        self.max_tries = 100
        self.scp = None
        self.client = None
        self.ssh_key = None
        self._load_ssh()

        for i in range(self.max_tries):
            try:
                self._connect()
            except NoValidConnectionsError as e:
                if i == self.max_tries - 1:
                    print("Reached max number of tries for ssh connection. ")
                    raise e
                continue
            break

    def _load_ssh(self):
        self.ssh_key = RSAKey.from_private_key_file(self.filepath)
        system(f'ssh-copy-id -i {self.filepath} {self.user}@{self.host}>/dev/null 2>&1')
        system(f'ssh-copy-id -i {self.filepath}.pub {self.user}@{self.host}>/dev/null 2>&1')

    def _connect(self):
        """ Conect to remote host """
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(self.host,
                            username=self.user,
                            key_filename=self.filepath,
                            look_for_keys=True,
                            timeout=5000)
        self.scp = SCPClient(self.client.get_transport())

    def disconnect(self):
        """ Close ssh connection """
        self.client.close()
        self.scp.close()

    def execute_commands(self, commands):
        """ Execute commands """
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            if stdout.channel.recv_exit_status() != 0:
                for line in stderr.readlines():
                    print(line)
                raise Exception
            else:
                for line in stdout.readlines():
                    print(line)

    def upload_files(self, files):
        """ Upload files to remote directory.
            __________
            files : [str], list of file paths to upload

        """

        for f in files:
            self.scp.put(f, recursive=True)
