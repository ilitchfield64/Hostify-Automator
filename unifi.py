## This program is a short script to blast a whole network to join
## any and all Unifi devices to the cloud management system
## Use with caution on New Unifi devices only
## IN theory it should only affect the Unifi devices, however a firewall
## may block traffic due to excesive pings


### Imports
from sys import exit
from os import system, name
import platform
import subprocess
import paramiko

### Declartaions
ip_string = 0
username = "ubnt"
password = "ubnt"
unifi_link = 'http://unifi.tech-keys.com:8080/inform'
pass_list = []
fail_list = []
#AP_pass_count = 0
e_log = open("ErrorLog.txt","w")
e_log.write("Starting Error Logging...\n")
c_log = open("ConsoleLog.txt","w")
c_log.write("Starting Console Output Log...\n")

### Functions

## Converts IP back to string for use elsewhere
def list_to_str(list1):
    string1 = str(list1[0]) + "." + str(list1[1]) + "." + str(list1[2]) + "." + str(list1[3])
    return string1

## Pings the remote host to determine if the AP is up
def pinger(host):

    # return True # this is for debugging REMOVE ME
    parameter = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)

    if response == 0:
        print("Ping!")
        return True
    else:
        print("Failed to Ping")
        return False

## This executes an SSH Sesh and runs a remote command MAY NEED TO ADD EXCEPTIONS TO THIS METHOD NEEDS TESTING
def AP_info_setter(user_name, pass_word, host, link):
   ## Creates the SSH Session
    c_log.write("Opening SSH on " + str(host))
    port = 22
    command = "mca-cli-op set-inform " + str(link) # This '/inform/ might not be needed if the link has it already
    #command = 'help'
    print(command)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user_name, pass_word)

    ## Runs remote command and prints the output
    stdin, stdout, stderr = ssh.exec_command(str(command))
    print(stdin)
    print(stdout)
    print(stderr)
    c_log.write(str(stdout) +'\n'+ str(stderr) + '\n')
    for line in stdout:
        print(line)
        c_log.write(str(line) + "\n")
    ## Closes the  SSH Sesh and prints the std terminal
    ssh.close()
    print(stdin)
    print(stdout)
    print(stderr)
    c_log.write(str(stderr) +'\n'+ str(stderr) + '\n')
    c_log.write(str(ip_string))
    
    # Need to lint the 'lines' variable to see if it says failure' 

##  Runs when any step fails and will output the failure to a log file in the PWD
def failure(ip_address):
    print("Fail")
    #fail_list.append(list_to_str(ip_address))
    #print(fail_list)
    e_log.write(ip_address + ": Failed\n")

############~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##########

### Main Loop 
def main():


## Input data for script   
    print()
    print()
    ip_string = input("Enter the Network Subnet for the Unifi Network: ")
    user = "ubnt"
    password = "ubnt"
   ## unifi_link = input("Enter the Unifi Cloud Link: ")

## Takes IP and breaks it up into a list
    ip_address = ip_string.split('.')
    ip_address[3] = int(ip_address[3])
    ip_address[3] = 98
    ip_string = list_to_str(ip_address)


# Some debug code for testing
    
#    print(ip_address[3])
   
#    print(ip_string)

#    pinger(ip_string)


### Primary loop

    ## The code will run from address in range x thru 254
    try:
        for ip_address[3] in range(100, 254):
            ip_string = list_to_str(ip_address)
        
            ## Tries to ping a remote host, and then attempts to open an SSH Session one success
            if pinger(list_to_str(ip_address)):
                print("Pass")
                ## The following method fails to a hard exit, need to add error exceptions if the command fails and to log the IP missed
                #Try this
                try:
                    AP_info_setter(username, password, list_to_str(ip_address), unifi_link) 
                    pass_list.append(list_to_str(ip_address))
                    ## Increment the counter up for passes
                    #global AP_pass_count += 1
                
                    # On try fail run failure() method. THE ERROR EXCEPTION FOR FAILING AN SSH SESSION MAY NEED TO BE IN THE AP_info_setter() METHOD
                except EOFError as e:
                    print(e)
                    failure(list_to_str(ip_address))
                    
                
                except paramiko.ssh_exception.AuthenticationException as e:
                    
                    print(e)
                    failure(list_to_str(ip_address))
                
                except paramiko.ssh_exception.NoValidConnectionsError as e:
                    print(e)
                    failure(list_to_str(ip_address)) 
                except TimeoutError as e:
                    print(e)
                    failure(list_to_str(ip_address))


            else:
                failure(list_to_str(ip_address))
            
    except KeyboardInterrupt as e:
        print("Intrrupted by User")
        e_log.write("Interupted by user\n" +str(e))
        c_log.write("Interupted by User\n")

        
    ## Shows the number of APs completed 
    #print("The numeber of APs passed is: " + AP_pass_count)
    print("Check Log file for any errors")
    e_log.close()
    c_log.close()

main()



