from sys import exit
from os import system, name
import platform
import subprocess
import paramiko
import spur


user_name = 'ubnt'
pass_word = 'ubnt'
link = 'http://unifi.tech-keys.com:8080/inform'


'''
shell = spur.SshShell(hostname='10.64.89.167', username="ubnt", password="ubnt")
with shell:
    result = shell.run(["mca-cli-op info"])
print(result.output)

'''








def AP_info_setter(user_name, pass_word, host, link):
   
    port = 22
    command = "mca-cli-op set-inform " + str(link) # This '/inform/ might not be needed if the link has it already
    #command = 'help'
    print(command)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user_name, pass_word)

    
    stdin, stdout, stderr = ssh.exec_command(str(command))
    print(stdin)
    print(stdout)
    print(stderr)
    for line in stdout:
        print(line)
    
    ssh.close()
    print(stdin)
    print(stdout)
    print(stderr)

AP_info_setter(user_name, pass_word, '10.64.89.167', link)
