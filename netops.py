import paramiko, requests, json, os, csv
from dotenv import load_dotenv
load_dotenv()

##constructors
def write_list_to_file(lst, filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write("%s\n" % item.strip())

cmd0 = "terminal length 0"
cmd1 = "show running-config"
ssh = paramiko.SSHClient()
with open('targets.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        for ipaddress in row:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("Attempting to establish SSH connection with " + ipaddress)
            try:
                ssh.connect(ipaddress, username = os.getenv('USERNAME'), password = os.getenv('PASSWORD'))
                stdin, stdout, stderr = ssh.exec_command(cmd0)
                stdin, stdout, stderr = ssh.exec_command(cmd1)
                output = stdout.readlines()
                write_list_to_file(output, ipaddress + '.config')
                ssh.close()
            except:
                print("Unable to establish SSH connection with " + ipaddress)